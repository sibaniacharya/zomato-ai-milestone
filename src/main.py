import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.config import Settings
from src.data.loader import DatasetLoader
from src.data.preprocessor import DataPreprocessor
from src.data.repository import RestaurantRepository
from src.services.filter import RestaurantFilter
from src.services.prompt_builder import PromptBuilder
from src.services.groq_client import GroqClient
from src.services.parser import ResponseParser
from src.services.enricher import RecommendationEnricher
from src.services.recommendation import RecommendationService
from src.api.routes import router, get_repository, get_recommendation_service
import threading
import os

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Global state
app_state = {}

def initialize_data(settings: Settings):
    try:
        # 1. Load & Preprocess Data
        loader = DatasetLoader(settings)
        raw_df = loader.load()
        
        preprocessor = DataPreprocessor(settings)
        restaurants = preprocessor.preprocess(raw_df)
        
        # 2. Setup Repository
        repository = RestaurantRepository(restaurants)
        app_state["repository"] = repository
        
        # 3. Setup Services
        filter_svc = RestaurantFilter(settings)
        prompt_builder = PromptBuilder(settings)
        groq_client = GroqClient(settings)
        parser = ResponseParser()
        enricher = RecommendationEnricher()
        
        recommendation_service = RecommendationService(
            settings, filter_svc, prompt_builder, groq_client, parser, enricher
        )
        app_state["recommendation_service"] = recommendation_service
        
        logger.info("Application successfully initialized.")
    except Exception as e:
        import traceback
        app_state["error"] = traceback.format_exc()
        logger.error(f"Failed to initialize data: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up Zomato AI Recommendation Backend...")
    settings = Settings()
    
    # Run data initialization in a background thread to prevent blocking server startup
    # This prevents the container from timing out or failing health checks
    thread = threading.Thread(target=initialize_data, args=(settings,))
    thread.daemon = True
    thread.start()
    
    yield
    # Cleanup if needed
    logger.info("Shutting down...")

app = FastAPI(
    title="Zomato AI Recommender API",
    description="Backend API for AI-powered restaurant recommendations.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_repo_safe():
    repo = app_state.get("repository")
    if not repo:
        raise HTTPException(status_code=503, detail="Server is still downloading and initializing data. Please try again in a few seconds.")
    return repo

def get_rec_svc_safe():
    svc = app_state.get("recommendation_service")
    if not svc:
        raise HTTPException(status_code=503, detail="Server is still downloading and initializing data. Please try again in a few seconds.")
    return svc

# Dependency overrides
app.dependency_overrides[get_repository] = get_repo_safe
app.dependency_overrides[get_recommendation_service] = get_rec_svc_safe

# Include router
app.include_router(router, prefix="/api")

@app.get("/debug")
async def debug_info():
    import os
    import hashlib
    try:
        data_dir = os.listdir("data") if os.path.exists("data") else []
        app_dir = os.listdir(".")
        file_size = os.path.getsize("data/fixed_restaurants.parquet") if os.path.exists("data/fixed_restaurants.parquet") else -1
        
        file_hash = None
        if os.path.exists("data/fixed_restaurants.parquet"):
            with open("data/fixed_restaurants.parquet", "rb") as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
                
        return {
            "status": "initializing" if "repository" not in app_state else "ready",
            "error": str(app_state.get("error")),
            "data_dir": data_dir,
            "app_dir": app_dir,
            "file_size": file_size,
            "file_hash": file_hash
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok"}

# Serve frontend static files
import os
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
