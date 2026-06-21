import logging
from typing import List
from src.config import Settings
from src.data.repository import RestaurantRepository
from src.models.preferences import UserPreferences
from src.models.recommendation import RecommendationResponse, RecommendationMetadata, Recommendation
from src.models.restaurant import Restaurant
from src.services.filter import RestaurantFilter
from src.services.prompt_builder import PromptBuilder
from src.services.groq_client import GroqClient
from src.services.parser import ResponseParser, ParseError
from src.services.enricher import RecommendationEnricher

logger = logging.getLogger(__name__)

class RecommendationService:
    def __init__(
        self,
        settings: Settings,
        filter_svc: RestaurantFilter,
        prompt_builder: PromptBuilder,
        groq_client: GroqClient,
        parser: ResponseParser,
        enricher: RecommendationEnricher,
    ):
        self.settings = settings
        self.filter = filter_svc
        self.prompt_builder = prompt_builder
        self.groq_client = groq_client
        self.parser = parser
        self.enricher = enricher

    def recommend(
        self,
        preferences: UserPreferences,
        repository: RestaurantRepository,
    ) -> RecommendationResponse:
        # 1. Filter candidates
        filter_result = self.filter.filter(repository.get_all(), preferences)
        
        candidates = filter_result.restaurants
        if not candidates:
            # Absolute zero results even after relaxations
            return RecommendationResponse(
                summary="We couldn't find any restaurants matching your expanded criteria.",
                recommendations=[],
                metadata=RecommendationMetadata(
                    candidates_considered=0,
                    filters_applied=filter_result.filters_applied,
                    relaxed_constraints=filter_result.relaxed_constraints,
                    model="none"
                )
            )

        # 2. Build prompt
        system_prompt, user_prompt = self.prompt_builder.build(
            preferences, candidates, self.settings.TOP_K_RECOMMENDATIONS
        )

        metadata = RecommendationMetadata(
            candidates_considered=filter_result.filtered_count,
            filters_applied=filter_result.filters_applied,
            relaxed_constraints=filter_result.relaxed_constraints,
            model=self.groq_client.model
        )

        # 3. Call Groq
        try:
            raw_response = self.groq_client.complete(system_prompt, user_prompt)
            candidate_ids = {r.id for r in candidates}
            
            # 4. Parse
            try:
                parsed = self.parser.parse(raw_response, candidate_ids)
            except ParseError as e:
                logger.warning(f"Parse error on first attempt: {e}. Retrying with low temp.")
                # Retry with low temp
                raw_response = self.groq_client.complete(system_prompt, user_prompt, low_temp=True)
                parsed = self.parser.parse(raw_response, candidate_ids)
                
            # 5. Enrich and return
            return self.enricher.enrich(parsed, candidates, metadata)
            
        except Exception as e:
            logger.error(f"LLM Pipeline completely failed: {e}. Falling back.")
            return self._fallback_ranking(candidates, self.settings.TOP_K_RECOMMENDATIONS, metadata)

    def _fallback_ranking(
        self, candidates: List[Restaurant], top_k: int, metadata: RecommendationMetadata
    ) -> RecommendationResponse:
        """Heuristic fallback when LLM fails."""
        metadata.fallback_used = True
        metadata.model = "fallback-heuristic"
        
        sorted_candidates = sorted(
            candidates, key=lambda r: (-r.rating, -r.votes)
        )

        seen_names = set()
        recommendations = []
        rank = 1
        for r in sorted_candidates:
            if r.name.lower() in seen_names:
                continue
            seen_names.add(r.name.lower())
            
            recommendations.append(
                Recommendation(
                    rank=rank,
                    name=r.name,
                    cuisine=", ".join(r.cuisines),
                    rating=r.rating,
                    estimated_cost=r.cost_for_two,
                    explanation=f"Highly rated {', '.join(r.cuisines)} restaurant in {r.location}."
                )
            )
            rank += 1
            if len(recommendations) >= top_k:
                break
        
        return RecommendationResponse(
            summary="Our AI assistant is temporarily unavailable, so we're showing you the top-rated restaurants matching your preferences.",
            recommendations=recommendations,
            metadata=metadata
        )
