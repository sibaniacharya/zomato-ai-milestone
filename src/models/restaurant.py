from dataclasses import dataclass

@dataclass
class Restaurant:
    id: str
    name: str
    location: str
    cuisines: list[str]
    cost_for_two: int
    rating: float
    votes: int = 0
    rest_type: str = ""
    budget_tier: str = ""  # derived: "low" | "medium" | "high"
