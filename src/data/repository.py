from typing import List, Optional
from src.models.restaurant import Restaurant

class RestaurantRepository:
    def __init__(self, restaurants: List[Restaurant]):
        self._restaurants = restaurants
        self._id_map = {r.id: r for r in restaurants}
        
        # Precompute distinct values
        self._locations = sorted(list(set(r.location for r in restaurants if r.location)))
        
        # Extract unique cuisines
        cuisines_set = set()
        for r in restaurants:
            for c in r.cuisines:
                cuisines_set.add(c)
        self._cuisines = sorted(list(cuisines_set))

    def get_all(self) -> List[Restaurant]:
        return self._restaurants

    def get_by_id(self, restaurant_id: str) -> Optional[Restaurant]:
        return self._id_map.get(restaurant_id)

    def get_distinct_locations(self) -> List[str]:
        return self._locations

    def get_distinct_cuisines(self) -> List[str]:
        return self._cuisines

    def count(self) -> int:
        return len(self._restaurants)
