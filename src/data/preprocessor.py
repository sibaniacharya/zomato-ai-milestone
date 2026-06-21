import pandas as pd
from typing import List
from src.config import Settings
from src.models.restaurant import Restaurant

class DataPreprocessor:
    def __init__(self, settings: Settings):
        self.settings = settings
        
        # Alias map for locations
        self.location_aliases = {
            "bangalore": "Bangalore",
            "bengaluru": "Bangalore",
            "delhi": "New Delhi",
            "new delhi": "New Delhi",
            "mumbai": "Mumbai",
            "pune": "Pune"
        }

    def preprocess(self, raw_df: pd.DataFrame) -> List[Restaurant]:
        """Full pipeline: clean, normalize, derive tiers, return Restaurant list."""
        
        # 1. Select and rename columns (assuming raw HF columns are similar to target)
        # Handle cases where column names might vary slightly
        col_map = {
            "name": "name", "Name": "name",
            "location": "location", "Location": "location", "city": "location",
            "cuisines": "cuisines", "Cuisines": "cuisines",
            "cost_for_two": "cost_for_two", "approx_cost(for two people)": "cost_for_two",
            "rating": "rating", "rate": "rating", "Aggregate rating": "rating",
            "votes": "votes", "Votes": "votes",
            "rest_type": "rest_type"
        }
        
        df = raw_df.rename(columns=col_map)
        
        restaurants = []
        seen = set()
        
        for idx, row in df.iterrows():
            try:
                # 2. Parse cuisines
                cuisines_val = row.get("cuisines", "")
                if pd.isna(cuisines_val):
                    cuisines_val = ""
                cuisines = self._parse_cuisines(str(cuisines_val))
                
                # 3. Coerce numerics
                rating_val = row.get("rating", 0)
                if pd.isna(rating_val) or str(rating_val).strip() in ["NEW", "-", ""]:
                    continue # Skip invalid ratings
                    
                rating = float(str(rating_val).split('/')[0].strip()) if '/' in str(rating_val) else float(rating_val)
                
                cost_val = row.get("cost_for_two", 0)
                if pd.isna(cost_val):
                    continue
                cost_str = str(cost_val).replace(",", "")
                cost = int(float(cost_str)) if cost_str.replace('.', '', 1).isdigit() else 0
                if cost <= 0:
                    continue
                
                # 4. Normalize locations
                location_val = row.get("location", "")
                if pd.isna(location_val) or not location_val:
                    continue
                location = self._normalize_location(str(location_val))
                
                name_val = str(row.get("name", "Unknown")).strip()
                
                # Deduplicate by name and location
                unique_key = (name_val.lower(), location.lower())
                if unique_key in seen:
                    continue
                seen.add(unique_key)
                
                # 5. Derive budget tier
                budget_tier = self._derive_budget_tier(cost)
                
                # Assign to model
                r = Restaurant(
                    id=str(idx),
                    name=name_val,
                    location=location,
                    cuisines=cuisines,
                    cost_for_two=cost,
                    rating=rating,
                    votes=int(row.get("votes", 0)),
                    rest_type=str(row.get("rest_type", "")),
                    budget_tier=budget_tier
                )
                restaurants.append(r)
            except Exception:
                # Silently skip malformed rows
                continue
                
        return restaurants

    def _parse_cuisines(self, cuisine_str: str) -> List[str]:
        if not cuisine_str:
            return []
        return [c.strip() for c in cuisine_str.split(",") if c.strip()]

    def _normalize_location(self, location: str) -> str:
        clean_loc = location.strip().lower()
        # Find partial match in aliases
        for alias, actual in self.location_aliases.items():
            if alias in clean_loc:
                return actual
        return location.strip().title()

    def _derive_budget_tier(self, cost: int) -> str:
        if cost <= self.settings.BUDGET_LOW_MAX:
            return "low"
        elif cost <= self.settings.BUDGET_MEDIUM_MAX:
            return "medium"
        else:
            return "high"
