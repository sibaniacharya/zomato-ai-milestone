from dataclasses import dataclass
from typing import Literal, Optional

@dataclass
class UserPreferences:
    location: str
    budget: Literal["low", "medium", "high"]
    min_rating: float
    cuisine: Optional[str] = None
    additional: Optional[str] = None
