import json
from typing import Tuple, List
from src.config import Settings
from src.models.preferences import UserPreferences
from src.models.restaurant import Restaurant

class PromptBuilder:
    def __init__(self, settings: Settings):
        self.settings = settings

    def build(
        self,
        preferences: UserPreferences,
        candidates: List[Restaurant],
        top_k: int = 5,
    ) -> Tuple[str, str]:
        system_prompt = (
            "You are a highly intelligent restaurant recommendation assistant. "
            "You MUST ONLY recommend restaurants from the provided CANDIDATES list. "
            "Do NOT invent, fabricate, or hallucinate restaurants. "
            "Your output MUST be a valid JSON object matching the requested schema."
        )

        candidates_json = [
            {
                "id": r.id,
                "name": r.name,
                "location": r.location,
                "cuisines": r.cuisines,
                "cost_for_two": r.cost_for_two,
                "rating": r.rating,
                "votes": r.votes
            }
            for r in candidates
        ]

        user_prompt = f"""
USER PREFERENCES:
- Location: {preferences.location}
- Budget Tier: {preferences.budget}
- Minimum Rating: {preferences.min_rating}
- Preferred Cuisine: {preferences.cuisine or 'Any'}
- Additional Notes: {preferences.additional or 'None'}

CANDIDATES:
{json.dumps(candidates_json, indent=2)}

TASK:
Based on the USER PREFERENCES, select the top {top_k} restaurants from the CANDIDATES list.
Return a JSON object strictly matching this schema:
{{
  "summary": "A brief 1-2 sentence summary explaining the recommendations overall.",
  "recommendations": [
    {{
      "id": "restaurant_id_here",
      "rank": 1,
      "explanation": "A 1-2 sentence compelling reason why this fits the user's preferences."
    }}
  ]
}}
"""
        return system_prompt, user_prompt
