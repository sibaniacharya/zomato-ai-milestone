import sys
import json
from src.config import Settings
from src.data.loader import DatasetLoader
from src.data.preprocessor import DataPreprocessor
from src.data.repository import RestaurantRepository
from src.services.filter import RestaurantFilter, PreferenceValidator
from src.services.prompt_builder import PromptBuilder
from src.services.groq_client import GroqClient
from src.services.parser import ResponseParser
from src.services.enricher import RecommendationEnricher
from src.services.recommendation import RecommendationService
from src.models.preferences import UserPreferences

def main():
    settings = Settings()
    print("Loading data...")
    loader = DatasetLoader(settings)
    raw_df = loader.load()
    
    preprocessor = DataPreprocessor(settings)
    restaurants = preprocessor.preprocess(raw_df)
    
    repository = RestaurantRepository(restaurants)
    
    validator = PreferenceValidator(repository.get_distinct_locations(), repository.get_distinct_cuisines())
    
    # Inputs:
    # Location: Bellandur
    # Rating: 4.2
    # Budget: 1500 -> 'medium'
    
    raw_prefs = UserPreferences(
        location="Bellandur",
        budget="medium",
        min_rating=4.2
    )
    
    prefs = validator.validate_and_normalize(raw_prefs)
    
    svc = RecommendationService(
        settings=settings,
        filter_service=RestaurantFilter(settings),
        prompt_builder=PromptBuilder(settings),
        groq_client=GroqClient(settings),
        parser=ResponseParser(),
        enricher=RecommendationEnricher()
    )
    
    print("Getting recommendations...")
    result = svc.recommend(prefs, repository)
    
    print("\n--- RESULTS ---")
    print(f"Summary: {result.summary}")
    for r in result.recommendations:
        print(f"\n{r.rank}. {r.name} (Rating: {r.rating}, Cost: {r.estimated_cost})")
        print(f"Cuisine: {r.cuisine}")
        print(f"Why: {r.explanation}")

if __name__ == "__main__":
    main()
