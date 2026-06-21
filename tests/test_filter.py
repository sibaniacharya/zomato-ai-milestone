import pytest
from src.models.restaurant import Restaurant
from src.models.preferences import UserPreferences
from src.services.filter import RestaurantFilter, PreferenceValidator, ValidationError
from src.config import Settings

@pytest.fixture
def settings():
    class TestSettings(Settings):
        GROQ_API_KEY: str = "test"
        MAX_CANDIDATES_FOR_LLM: int = 5
    return TestSettings()

@pytest.fixture
def restaurants():
    return [
        Restaurant(id="1", name="R1", location="Bangalore", cuisines=["Italian", "Chinese"], cost_for_two=1000, rating=4.5, votes=100, budget_tier="medium"),
        Restaurant(id="2", name="R2", location="Bangalore", cuisines=["Indian"], cost_for_two=400, rating=4.0, votes=50, budget_tier="low"),
        Restaurant(id="3", name="R3", location="Delhi", cuisines=["Italian"], cost_for_two=1200, rating=4.8, votes=200, budget_tier="medium"),
        Restaurant(id="4", name="R4", location="Bangalore", cuisines=["Continental"], cost_for_two=2000, rating=3.5, votes=10, budget_tier="high"),
        Restaurant(id="5", name="R5", location="Bangalore", cuisines=["Italian"], cost_for_two=1000, rating=3.0, votes=5, budget_tier="medium"),
        Restaurant(id="6", name="R6", location="Bangalore", cuisines=["Italian"], cost_for_two=1000, rating=4.2, votes=300, budget_tier="medium"),
        Restaurant(id="7", name="R7", location="Bangalore", cuisines=["Italian"], cost_for_two=1000, rating=4.2, votes=500, budget_tier="medium"),
    ]

@pytest.fixture
def filter_service(settings):
    return RestaurantFilter(settings)

def test_filter_by_location(filter_service, restaurants):
    prefs = UserPreferences(location="Delhi", budget="medium", min_rating=4.0)
    res = filter_service.filter(restaurants, prefs)
    assert len(res.restaurants) == 1
    assert res.restaurants[0].id == "3"

def test_filter_by_budget_tier(filter_service, restaurants):
    prefs = UserPreferences(location="Bangalore", budget="low", min_rating=0.0)
    res = filter_service.filter(restaurants, prefs)
    assert len(res.restaurants) == 1
    assert res.restaurants[0].id == "2"

def test_filter_by_min_rating(filter_service, restaurants):
    prefs = UserPreferences(location="Bangalore", budget="high", min_rating=4.0)
    res = filter_service.filter(restaurants, prefs)
    assert "budget" in res.relaxed_constraints

def test_filter_by_cuisine_partial_match(filter_service, restaurants):
    prefs = UserPreferences(location="Bangalore", budget="medium", min_rating=4.0, cuisine="Italian")
    res = filter_service.filter(restaurants, prefs)
    assert len(res.restaurants) == 3

def test_relaxation_cuisine_first(filter_service, restaurants):
    prefs = UserPreferences(location="Bangalore", budget="medium", min_rating=4.0, cuisine="Mexican")
    res = filter_service.filter(restaurants, prefs)
    assert "cuisine" in res.relaxed_constraints
    assert "budget" not in res.relaxed_constraints
    assert len(res.restaurants) > 0

def test_relaxation_records_constraints(filter_service, restaurants):
    prefs = UserPreferences(location="Bangalore", budget="low", min_rating=4.5, cuisine="Mexican")
    res = filter_service.filter(restaurants, prefs)
    assert "cuisine" in res.relaxed_constraints
    assert "budget" in res.relaxed_constraints
    assert len(res.restaurants) == 1
    assert res.restaurants[0].id == "1"

def test_candidate_cap(filter_service, restaurants):
    # Temporarily force the cap to 2 to bypass .env overrides
    filter_service.settings.MAX_CANDIDATES_FOR_LLM = 2
    prefs = UserPreferences(location="Bangalore", budget="medium", min_rating=0.0)
    res = filter_service.filter(restaurants, prefs)
    assert len(res.restaurants) == 2

def test_sort_rating_desc_votes_desc(filter_service, restaurants):
    prefs = UserPreferences(location="Bangalore", budget="medium", min_rating=4.0, cuisine="Italian")
    res = filter_service.filter(restaurants, prefs)
    assert res.restaurants[0].id == "1"
    assert res.restaurants[1].id == "7"
    assert res.restaurants[2].id == "6"

def test_validation_invalid_location():
    validator = PreferenceValidator(["Bangalore", "Delhi"], ["Italian"])
    prefs = UserPreferences(location="New York", budget="medium", min_rating=4.0)
    with pytest.raises(ValidationError) as exc:
        validator.validate_and_normalize(prefs)
    assert "Invalid location" in str(exc.value)

def test_validation_invalid_budget():
    validator = PreferenceValidator(["Bangalore"], ["Italian"])
    prefs = UserPreferences(location="Bangalore", budget="super_high", min_rating=4.0) # type: ignore
    with pytest.raises(ValidationError) as exc:
        validator.validate_and_normalize(prefs)
    assert "Invalid budget" in str(exc.value)

def test_validation_rating_out_of_range():
    validator = PreferenceValidator(["Bangalore"], ["Italian"])
    prefs = UserPreferences(location="Bangalore", budget="medium", min_rating=6.0)
    with pytest.raises(ValidationError) as exc:
        validator.validate_and_normalize(prefs)
    assert "Invalid min_rating" in str(exc.value)
