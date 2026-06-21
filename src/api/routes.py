from fastapi import APIRouter, Depends, HTTPException
from typing import List
from src.api.schemas import RecommendationRequest, RecommendationResponseSchema
from src.models.preferences import UserPreferences
from src.data.repository import RestaurantRepository
from src.services.recommendation import RecommendationService

router = APIRouter()

# Dependency injection placeholders (these will be overridden in main.py)
def get_repository() -> RestaurantRepository:
    raise NotImplementedError()

def get_recommendation_service() -> RecommendationService:
    raise NotImplementedError()

@router.get("/locations", response_model=List[str], tags=["Data"])
def get_locations(repo: RestaurantRepository = Depends(get_repository)):
    return repo.get_distinct_locations()

@router.get("/cuisines", response_model=List[str], tags=["Data"])
def get_cuisines(repo: RestaurantRepository = Depends(get_repository)):
    return repo.get_distinct_cuisines()

@router.post("/recommend", response_model=RecommendationResponseSchema, tags=["Recommendation"])
def recommend_restaurants(
    req: RecommendationRequest,
    repo: RestaurantRepository = Depends(get_repository),
    service: RecommendationService = Depends(get_recommendation_service)
):
    try:
        preferences = UserPreferences(
            location=req.location,
            budget=req.budget,
            min_rating=req.min_rating,
            cuisine=req.cuisine,
            additional=req.additional
        )
        
        response = service.recommend(preferences, repo)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
