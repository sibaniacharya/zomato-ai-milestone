from pydantic import BaseModel, Field
from typing import Literal, Optional, List, Dict, Any

class RecommendationRequest(BaseModel):
    location: str = Field(..., description="City or location (e.g. Bangalore)")
    budget: Literal["low", "medium", "high"] = Field(..., description="Budget tier")
    min_rating: float = Field(0.0, ge=0.0, le=5.0, description="Minimum acceptable rating")
    cuisine: Optional[str] = Field(None, description="Preferred cuisine")
    additional: Optional[str] = Field(None, max_length=500, description="Any additional preferences")

class RecommendationItemSchema(BaseModel):
    rank: int
    name: str
    cuisine: str
    rating: float
    estimated_cost: int
    explanation: str

class RecommendationMetadataSchema(BaseModel):
    candidates_considered: int
    filters_applied: Dict[str, Any]
    relaxed_constraints: List[str]
    model: str
    fallback_used: bool

class RecommendationResponseSchema(BaseModel):
    summary: Optional[str]
    recommendations: List[RecommendationItemSchema]
    metadata: RecommendationMetadataSchema
