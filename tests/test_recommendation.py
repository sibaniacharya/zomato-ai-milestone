import pytest
import json
from src.config import Settings
from src.models.preferences import UserPreferences
from src.models.restaurant import Restaurant
from src.services.filter import RestaurantFilter
from src.services.prompt_builder import PromptBuilder
from src.services.parser import ResponseParser
from src.services.enricher import RecommendationEnricher
from src.services.recommendation import RecommendationService
from src.data.repository import RestaurantRepository

class DummyGroqClient:
    def __init__(self, raw_response: str, should_fail: bool = False):
        self.raw_response = raw_response
        self.should_fail = should_fail
        self.model = "dummy-model"
        
    def complete(self, sys_p, usr_p, temperature=None):
        if self.should_fail:
            raise Exception("API Error")
        return self.raw_response

@pytest.fixture
def settings():
    class TestSettings(Settings):
        GROQ_API_KEY: str = "test"
        MAX_CANDIDATES_FOR_LLM: int = 5
        TOP_K_RECOMMENDATIONS: int = 2
    return TestSettings()

@pytest.fixture
def repository():
    rests = [
        Restaurant(id="1", name="R1", location="Bangalore", cuisines=["Italian"], cost_for_two=1000, rating=4.5, votes=100, budget_tier="medium"),
        Restaurant(id="2", name="R2", location="Bangalore", cuisines=["Chinese"], cost_for_two=800, rating=4.0, votes=50, budget_tier="medium"),
        Restaurant(id="3", name="R3", location="Delhi", cuisines=["Indian"], cost_for_two=500, rating=4.8, votes=200, budget_tier="low"),
    ]
    return RestaurantRepository(rests)

@pytest.fixture
def preferences():
    return UserPreferences(location="Bangalore", budget="medium", min_rating=0.0)

def test_recommend_happy_path(settings, repository, preferences):
    raw_llm = json.dumps({
        "summary": "Great picks.",
        "recommendations": [
            {"id": "1", "rank": 1, "explanation": "Best Italian."},
            {"id": "2", "rank": 2, "explanation": "Good Chinese."}
        ]
    })
    groq_client = DummyGroqClient(raw_llm, should_fail=False)
    
    svc = RecommendationService(
        settings=settings,
        filter_service=RestaurantFilter(settings),
        prompt_builder=PromptBuilder(settings),
        groq_client=groq_client, # type: ignore
        parser=ResponseParser(),
        enricher=RecommendationEnricher()
    )
    
    res = svc.recommend(preferences, repository)
    
    assert res.summary == "Great picks."
    assert len(res.recommendations) == 2
    assert res.recommendations[0].name == "R1"
    assert res.metadata.fallback_used is False
    assert res.metadata.model == "dummy-model"

def test_recommend_fallback_on_groq_failure(settings, repository, preferences):
    groq_client = DummyGroqClient("", should_fail=True)
    
    svc = RecommendationService(
        settings=settings,
        filter_service=RestaurantFilter(settings),
        prompt_builder=PromptBuilder(settings),
        groq_client=groq_client, # type: ignore
        parser=ResponseParser(),
        enricher=RecommendationEnricher()
    )
    
    res = svc.recommend(preferences, repository)
    
    assert "AI explanations unavailable" in (res.summary or "")
    assert len(res.recommendations) == 2
    assert res.recommendations[0].name == "R1"
    assert res.recommendations[1].name == "R2"
    assert res.metadata.fallback_used is True
    assert res.metadata.model == "heuristic_fallback"
