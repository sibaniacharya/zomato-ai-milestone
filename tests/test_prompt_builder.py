import pytest
from src.config import Settings
from src.models.preferences import UserPreferences
from src.models.restaurant import Restaurant
from src.services.prompt_builder import PromptBuilder

@pytest.fixture
def settings():
    return Settings(GROQ_API_KEY="test")

@pytest.fixture
def builder(settings):
    return PromptBuilder(settings)

@pytest.fixture
def preferences():
    return UserPreferences(location="Bangalore", budget="medium", min_rating=4.0, cuisine="Italian", additional="Good for dates")

@pytest.fixture
def candidates():
    return [
        Restaurant(id="1", name="R1", location="Bangalore", cuisines=["Italian"], cost_for_two=1000, rating=4.5),
        Restaurant(id="2", name="R2", location="Bangalore", cuisines=["Italian"], cost_for_two=1200, rating=4.2),
    ]

def test_prompt_contains_preferences(builder, preferences, candidates):
    sys_p, usr_p = builder.build(preferences, candidates, top_k=2)
    assert "Bangalore" in usr_p
    assert "medium" in usr_p
    assert "4.0" in usr_p
    assert "Italian" in usr_p
    assert "Good for dates" in usr_p

def test_prompt_contains_all_candidates(builder, preferences, candidates):
    sys_p, usr_p = builder.build(preferences, candidates, top_k=2)
    assert '"id": "1"' in usr_p
    assert '"name": "R1"' in usr_p
    assert '"id": "2"' in usr_p
    assert '"name": "R2"' in usr_p

def test_prompt_json_instruction(builder, preferences, candidates):
    sys_p, usr_p = builder.build(preferences, candidates, top_k=2)
    assert "valid JSON object" in sys_p

def test_prompt_anti_hallucination(builder, preferences, candidates):
    sys_p, usr_p = builder.build(preferences, candidates, top_k=2)
    assert "Only recommend restaurants from the CANDIDATES list" in sys_p
    assert "Do not invent or fabricate" in sys_p
