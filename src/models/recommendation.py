from dataclasses import dataclass
from typing import Any, List, TypedDict, Optional
from src.models.restaurant import Restaurant

@dataclass
class FilterResult:
    restaurants: List[Restaurant]
    filters_applied: dict[str, Any]
    relaxed_constraints: List[str]
    original_count: int
    filtered_count: int

@dataclass
class Recommendation:
    rank: int
    name: str
    cuisine: str
    rating: float
    estimated_cost: int
    explanation: str

@dataclass
class RecommendationMetadata:
    candidates_considered: int
    filters_applied: dict[str, Any]
    relaxed_constraints: List[str]
    model: str
    fallback_used: bool = False

@dataclass
class RecommendationResponse:
    summary: Optional[str]
    recommendations: List[Recommendation]
    metadata: RecommendationMetadata

class LLMRecommendationItem(TypedDict):
    id: str
    rank: int
    explanation: str

class LLMResponse(TypedDict):
    summary: str
    recommendations: List[LLMRecommendationItem]
