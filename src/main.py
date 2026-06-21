import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
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

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Global state
app_state = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up Zomato AI Recommendation Backend...")
    settings = Settings()
    
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

# Dependency overrides
app.dependency_overrides[get_repository] = lambda: app_state["repository"]
app.dependency_overrides[get_recommendation_service] = lambda: app_state["recommendation_service"]

# Include router
app.include_router(router, prefix="/api")

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok"}

# Serve frontend static files
import os
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(frontend_dir, "index.html"))
