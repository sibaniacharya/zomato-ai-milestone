import logging
from typing import List, Any
from src.config import Settings
from src.models.restaurant import Restaurant
from src.models.preferences import UserPreferences
from src.models.recommendation import FilterResult

logger = logging.getLogger(__name__)

class RestaurantFilter:
    def __init__(self, settings: Settings):
        self.settings = settings

    def filter(
        self,
        restaurants: List[Restaurant],
        preferences: UserPreferences,
    ) -> FilterResult:
        original_count = len(restaurants)
        relaxed_constraints = []
        filters_applied = {
            "location": preferences.location,
            "budget": preferences.budget,
            "min_rating": preferences.min_rating,
        }
        if preferences.cuisine:
            filters_applied["cuisine"] = preferences.cuisine
            
        # 1. Location (hard requirement)
        filtered = [r for r in restaurants if r.location.lower() == preferences.location.lower()]
        
        # 2. Cuisine (relaxable)
        if preferences.cuisine:
            cuisine_filtered = [r for r in filtered if any(preferences.cuisine.lower() in c.lower() for c in r.cuisines)]
            if not cuisine_filtered:
                relaxed_constraints.append("cuisine")
                logger.info(f"Zero results for cuisine '{preferences.cuisine}'. Relaxing constraint.")
            else:
                filtered = cuisine_filtered
                
        # 3. Budget (relaxable)
        budget_filtered = [r for r in filtered if r.budget_tier == preferences.budget]
        if not budget_filtered:
            relaxed_constraints.append("budget")
            logger.info(f"Zero results for budget '{preferences.budget}'. Relaxing constraint.")
        else:
            filtered = budget_filtered
            
        # 4. Minimum Rating (relaxable)
        rating_filtered = [r for r in filtered if r.rating >= preferences.min_rating]
        if not rating_filtered and filtered:
            relaxed_constraints.append("min_rating")
            logger.info(f"Zero results for min_rating >= {preferences.min_rating}. Relaxing constraint.")
        else:
            filtered = rating_filtered
            
        # 5. Sort & Cap
        filtered.sort(key=lambda x: (-x.rating, -x.votes))
        capped = filtered[:self.settings.MAX_CANDIDATES_FOR_LLM]
        
        return FilterResult(
            restaurants=capped,
            filters_applied=filters_applied,
            relaxed_constraints=relaxed_constraints,
            original_count=original_count,
            filtered_count=len(capped)
        )
