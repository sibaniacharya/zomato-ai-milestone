import pytest
import pandas as pd
from src.config import Settings
from src.data.preprocessor import DataPreprocessor

@pytest.fixture
def settings():
    return Settings(GROQ_API_KEY="test_key")

@pytest.fixture
def preprocessor(settings):
    return DataPreprocessor(settings)

def test_parse_cuisines_splits_comma_separated(preprocessor):
    result = preprocessor._parse_cuisines("Italian, Chinese")
    assert result == ["Italian", "Chinese"]

def test_parse_cuisines_single(preprocessor):
    result = preprocessor._parse_cuisines("Italian")
    assert result == ["Italian"]

def test_parse_cuisines_empty(preprocessor):
    result = preprocessor._parse_cuisines("")
    assert result == []

def test_normalize_location_titlecase(preprocessor):
    result = preprocessor._normalize_location("  bangalore ")
    assert result == "Bangalore"

def test_budget_tier_boundaries(preprocessor):
    assert preprocessor._derive_budget_tier(500) == "low"
    assert preprocessor._derive_budget_tier(501) == "medium"
    assert preprocessor._derive_budget_tier(1500) == "medium"
    assert preprocessor._derive_budget_tier(1501) == "high"

def test_full_preprocess_returns_restaurants(preprocessor):
    df = pd.DataFrame([
        {
            "name": "Test Place",
            "location": "Bangalore",
            "cuisines": "Italian",
            "cost_for_two": "1000",
            "rating": "4.5/5",
            "votes": "100",
            "rest_type": "Casual Dining"
        }
    ])
    
    result = preprocessor.preprocess(df)
    assert len(result) == 1
    r = result[0]
    assert r.name == "Test Place"
    assert r.location == "Bangalore"
    assert r.cuisines == ["Italian"]
    assert r.cost_for_two == 1000
    assert r.rating == 4.5
    assert r.budget_tier == "medium"
