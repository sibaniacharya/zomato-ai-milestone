from typing import List
from src.models.recommendation import (
    LLMResponse,
    Recommendation,
    RecommendationResponse,
    RecommendationMetadata
)
from src.models.restaurant import Restaurant

class RecommendationEnricher:
    def enrich(
        self,
        llm_response: LLMResponse,
        candidates: List[Restaurant],
        metadata: RecommendationMetadata,
    ) -> RecommendationResponse:
        candidate_map = {r.id: r for r in candidates}
        
        seen_names = set()
        enriched_recommendations = []
        rank = 1
        for item in sorted(llm_response["recommendations"], key=lambda x: x["rank"]):
            if str(item["id"]) not in candidate_map:
                continue
                
            r_obj = candidate_map[str(item["id"])]
            
            name_lower = r_obj.name.lower()
            if name_lower in seen_names:
                continue
            seen_names.add(name_lower)
            
            rec = Recommendation(
                rank=rank,
                name=r_obj.name,
                cuisine=", ".join(r_obj.cuisines),
                rating=r_obj.rating,
                estimated_cost=r_obj.cost_for_two,
                explanation=item["explanation"]
            )
            enriched_recommendations.append(rec)
            rank += 1
            
        return RecommendationResponse(
            summary=llm_response["summary"],
            recommendations=enriched_recommendations,
            metadata=metadata
        )
