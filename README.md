AI-Powered Restaurant Recommendation System (Zomato Use Case)
You are tasked with building an AI-powered restaurant recommendation service inspired by Zomato. The system should intelligently suggest restaurants based on user preferences by combining structured data with a Large Language Model (LLM).
Objective
Design and implement an application that:
Takes user preferences (such as location, budget, cuisine, and ratings)
Uses a real-world dataset of restaurants
Leverages an LLM to generate personalized, human-like recommendations
Displays clear and useful results to the user
System Workflow
Data Ingestion
Load and preprocess the Zomato dataset from Hugging Face (https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation )
Extract relevant fields such as restaurant name, location, cuisine, cost, rating, etc.
User Input
Collect user preferences:
Location (e.g., Delhi, Bangalore)
Budget (low, medium, high)
Cuisine (e.g., Italian, Chinese)
Minimum rating
Any additional preferences (e.g., family-friendly, quick service)
Integration Layer
Filter and prepare relevant restaurant data based on user input
Pass structured results into an LLM prompt
Design a prompt that helps the LLM reason and rank options
Recommendation Engine
Use the LLM to:
Rank restaurants
Provide explanations (why each recommendation fits)
Optionally summarize choices
Output Display
Present top recommendations in a user-friendly format:
Restaurant Name
Cuisine
Rating
Estimated Cost
AI-generated explanation


Diagram
AI Tools 
https://cursor.com/download 
https://antigravity.google/product/antigravity-ide (ANTIGRAVITY IDE) (PRO – JIO SIM) https://www.jio.com/google-gemini-offer/ 
https://qoder.com/ 

FOR GENERATING CONTEXT FILES in antigravity → Use Pro model or claude opus 
API Key
https://groq.com/ → Free API key → Create API key 
https://aistudio.google.com/api-keys 

Frontend / Backend
Backend 
Python, FastAPI
Nodejs, expressjs
Java, Spring Boot, C#, .NET 

Frontend
Streamlit → Basic UI 
React, Vite, Next.js → Good quality UI 
Steps
CONTEXT SETUP 
Docs folder 
problemStatement.txt → Basic problem statement of the project
context.md → stores the necessary context of the project 
architecture.md → detailed description of the project building 
implementation-plan.md → phase-wise implementation plan 
edge-case.md → corner scenario (LIVING DOCUMENT)
PROMPT
Generate a context.md which stores the entire context of @docs/problemStatement.txt 
Generate a detailed architecture.md using @docs/context.md  
LLM used in this project will be Groq, update it in the @docs/architecture.md 
Generate a phase-wise implementation-plan.md using the @docs/architecture.md and @docs/context.md 
Generate an edge-case.md for this project which contains all the corner scenarios
Implement phase0 as per the @docs/implementation-plan.md  
Implement phase1 as per the @docs/implementation-plan.md 
Implement phase2 as per the @docs/implementation-plan.md 
Implement phase3 as per the @docs/implementation-plan.md 

— GET the API key from https://groq.com/ and update in it .env 
Ask cursor to create .env.example or .env

In data location is Bangalore, ideally we should have indiranagar, bellandur etc in place or location as they will be the required input later on (YOU)
Location - Bellandur
Rating - 4.2
Budget - 1500
Predict top5 restaurants for these input with the help of LLM, API key is present in .env
In @docs/implementation-plan.md we want to have 2 different phases for backend and frontend. We want a good quality frontend for this application.
Implement phase4 backend part 1 as per the @docs/implementation-plan.md 
Using the @docs/context.md @docs/architecture.md
generate a prompt for google stitch for designing the frontend
PROMPT is below 
Using@stitch_zomato_ai_recommendations folder design and basic images of the website are present use them and
Images of food are currently not required so we can skip them
In locations there should be a dropdown rather than text input.
implement frontend as per the @docs/implementation-plan.md
MANUAL TESTING
run the entire project  
Open the project URL → http://localhost:3000 (URL can be different for you) 
stop the project 
For MG road and other places we notices duplicate entries are coming in the final result, ideally unique restaurants we should return  
PUSH the code to github 
CHECK .gitignore file is present 
PUSH the code to github - https://github.com/saksham20189575/milestone-zomato.git 


PROMPT for stitch 
Design a desktop-first web application home screen for an AI-powered restaurant recommendation product inspired by Zomato, optimized for laptop screens (1280px–1440px width), where users set dining preferences in a left panel and see ranked restaurant suggestions with AI-written explanations in a right panel.
Include a full-width top navigation bar with a food/dining logo on the left, product title "Zomato AI Recommendations", and tagline "Find your perfect restaurant" aligned to the right.
Include a centered main layout with max-width 1200px split into two columns: left column (40%) titled "Your preferences" containing a compact form with searchable location dropdown, budget dropdown with helper labels (Low under ₹500, Medium ₹501–1500, High above ₹1500), optional cuisine dropdown defaulting to "Any cuisine", minimum rating slider from 0.0 to 5.0 with live value label, multiline text area for additional preferences with placeholder "e.g. family-friendly, quick service", and a full-width primary button "Get Recommendations".
Include a right column (60%) titled "Recommendations" showing applied filter chips (location, budget, cuisine, min rating), an AI summary banner with subtle sparkle icon and quote-style text, and a vertical list of up to 5 recommendation cards each with rank badge (#1 gold, #2 silver, #3 bronze), bold restaurant name, cuisine pill tags, star rating with numeric score, cost formatted as "₹1,200 for two", and a 2–3 line AI explanation, with subtle hover lift on each card.
Include supporting UI states within the same screen: empty state in the right column before search ("Your top picks will appear here"), loading state with skeleton cards and message "AI is ranking restaurants for you…", empty results state with "No restaurants matched your filters" and suggestions to broaden search, amber warning banner when filters were relaxed, red inline validation errors below form fields with tappable location suggestion chips, and a dismissible error alert bar below the header for server failures.
Include a simple centered footer with muted copyright text.
Style: Zomato-inspired warm red primary (#E23744), white page background, light gray (#F8F8F8) panel backgrounds, dark text (#1C1C1C), Inter or modern sans-serif typography, subtle card shadows, generous 24–32px spacing, professional food-discovery mood, polished consumer product not a developer prototype.
Optimize for desktop web and laptop browsing at 1280px+, mouse hover interactions on cards and buttons, clear left-form right-results split, no mobile stacking, WCAG AA color contrast, keyboard-navigable form controls.

Basic INTRO steps
– Any md file (PREVIEW)
→ Ctrl + Shift + V (Windows)
→ Mac → Cmd + Shift + V 

Mentioning FILE → use @ 

Extension for Diagrams → Mermaid


Architecture

Architecture: AI-Powered Restaurant Recommendation System
This document describes the technical architecture for the Zomato-inspired restaurant recommendation service defined in context.md. The system combines structured restaurant data from Hugging Face with Groq LLM inference to produce personalized, explainable recommendations.

1. Architecture Goals
Goal
Description
Separation of concerns
Data loading, filtering, LLM reasoning, and presentation are isolated modules with clear interfaces.
Deterministic pre-filtering
Hard constraints (location, budget, rating) are applied before the LLM to reduce token cost and hallucination risk.
Explainability
Every recommendation includes an LLM-generated rationale tied to user preferences.
Extensibility
Swap UI frameworks or data sources without rewriting core logic; LLM access is isolated behind a Groq adapter.
Testability
Pure functions for filtering/ranking prep; mockable LLM adapter for unit tests.


3. Component Architecture
3.1 Data Ingestion Layer
Responsibility: Load, normalize, and cache the Zomato dataset once at startup (or on first request).
Component
Role
DatasetLoader
Fetches ManikaSaini/zomato-restaurant-recommendation via datasets (Hugging Face).
DataPreprocessor
Maps raw columns to a canonical schema, handles nulls, normalizes text fields.
RestaurantRepository
In-memory query interface over the preprocessed dataset.

Canonical restaurant schema:
Restaurant = {
    "id": str,              # stable identifier (index or dataset id)
    "name": str,
    "location": str,        # city / locality
    "cuisines": list[str],  # e.g. ["Italian", "Continental"]
    "cost_for_two": int,    # numeric cost indicator
    "rating": float,        # e.g. 4.2
    "votes": int,           # optional: popularity signal
    "rest_type": str,       # optional: casual dining, cafe, etc.
}

Preprocessing steps:
Download dataset split (typically train).
Select and rename relevant columns to the canonical schema.
Parse cuisine strings into lists (e.g. "Italian, Chinese" → ["Italian", "Chinese"]).
Coerce rating and cost to numeric types; drop or impute invalid rows.
Normalize location strings (trim, title-case, alias map for city names).
Derive budget_tier from cost_for_two using configurable thresholds:
Tier
Typical cost_for_two range (INR)
low
≤ 500
medium
501 – 1500
high
> 1500

Thresholds should be tuned after inspecting the actual dataset distribution.
Caching strategy: Load once into a pandas DataFrame or list of Restaurant objects. Persist a local parquet/CSV snapshot to avoid repeated Hugging Face downloads during development.

3.2 User Input Layer
Responsibility: Collect, validate, and normalize user preferences.
Input model:
UserPreferences = {
    "location": str,           # required
    "budget": str,             # "low" | "medium" | "high"
    "cuisine": str | None,     # optional primary cuisine
    "min_rating": float,       # e.g. 3.5
    "additional": str | None,  # free-text: "family-friendly, quick service"
}

Component
Role
PreferenceForm
UI form or CLI prompt collecting fields.
PreferenceValidator
Enforces required fields, enum values, rating bounds.
PreferenceNormalizer
Lowercases cuisine, maps city aliases, trims free text.

Validation rules:
location — non-empty; must match at least one value in the dataset (or suggest closest matches).
budget — one of low, medium, high.
min_rating — float in [0.0, 5.0].
cuisine — optional; fuzzy match against known cuisine vocabulary extracted from dataset.
additional — optional free text passed through to the LLM for soft matching.

3.3 Integration Layer
Responsibility: Apply hard filters, rank candidates heuristically, and assemble the LLM prompt.
This layer sits between structured data and the LLM. It ensures the model only reasons over a bounded, relevant candidate set.
3.3.1 Restaurant Filter
Applies deterministic filters in sequence:
all restaurants
  → filter by location (exact or case-insensitive match)
  → filter by budget tier
  → filter by min_rating
  → filter by cuisine (if provided; match if cuisine in restaurant.cuisines)
  → sort by rating desc, then votes desc
  → take top N candidates (default N = 15–20)

Component
Role
RestaurantFilter
Executes filter pipeline; returns list[Restaurant].
CandidateSelector
Caps result count and applies tie-breaking.

If zero candidates remain, relax constraints in order: cuisine → budget → min_rating, and surface a warning to the user.
3.3.2 Prompt Builder
Constructs a structured prompt containing:
System instructions — role, output format (JSON), ranking criteria.
User preferences — serialized UserPreferences.
Candidate restaurants — compact JSON array of filtered restaurants.
Task — rank top K (e.g. 5), explain each pick, optionally summarize.
Design principles:
Require JSON output from the LLM for reliable parsing.
Include restaurant id in candidates so explanations map back to structured data.
Instruct the model to only recommend from the provided list (no fabrication).
Pass additional preferences as soft signals the LLM may use in ranking/explanation.
Example prompt structure (conceptual):
[System]
You are a restaurant recommendation assistant for Indian cities.
Rank restaurants from the CANDIDATES list only. Return valid JSON.

[User Preferences]
{ location, budget, cuisine, min_rating, additional }

[Candidates]
[ { id, name, location, cuisines, cost_for_two, rating }, ... ]

[Task]
Return top 5 restaurants as JSON:
{
  "summary": "...",
  "recommendations": [
    {
      "id": "...",
      "rank": 1,
      "explanation": "..."
    }
  ]
}


3.4 Recommendation Engine (LLM Layer)
Responsibility: Invoke the LLM, handle retries, parse and validate the response, merge with structured data.
Component
Role
LLMClient
Thin adapter over the Groq API via the official groq Python SDK.
RecommendationService
Orchestrates prompt → LLM → parse → enrich.
ResponseParser
Parses JSON; validates schema; handles malformed output.
RecommendationEnricher
Joins LLM ranks/explanations with full restaurant records.

Output model:
Recommendation = {
    "rank": int,
    "name": str,
    "cuisine": str,           # joined cuisine string for display
    "rating": float,
    "estimated_cost": int,    # cost_for_two
    "explanation": str,       # LLM-generated
}

RecommendationResponse = {
    "summary": str | None,
    "recommendations": list[Recommendation],
    "metadata": {
        "candidates_considered": int,
        "filters_applied": dict,
        "model": str,
    }
}

Reliability patterns:
Pattern
Purpose
Structured output / JSON mode
Reduce parse failures.
Retry with temperature reduction
Recover from invalid JSON.
Fallback ranking
If LLM fails, return heuristic top-K by rating with a generic explanation.
Idempotency
Same preferences + same dataset snapshot → reproducible candidate set.

LLM is not used for:
Loading data
Hard filtering by location/budget/rating
Inventing restaurants not in the candidate list
Groq Integration
Groq is the sole LLM provider for this project. The LLMClient wraps Groq's chat completions API and is configured via environment variables.
Setting
Default
Notes
SDK
groq
Official Python client (pip install groq).
API key
GROQ_API_KEY
Required; set in .env, never committed.
Model
llama-3.3-70b-versatile
Strong reasoning for ranking and explanations.
Fallback model
llama-3.1-8b-instant
Optional faster/cheaper alternative for dev.
Temperature
0.3
Low enough for consistent JSON; retry with 0.1 on parse failure.

Client usage (conceptual):
from groq import Groq

client = Groq(api_key=settings.GROQ_API_KEY)

response = client.chat.completions.create(
    model=settings.GROQ_MODEL,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ],
    temperature=settings.GROQ_TEMPERATURE,
    response_format={"type": "json_object"},  # when supported by model
)

Groq-specific considerations:
Groq offers very low latency inference — suitable for interactive UI feedback.
Enforce JSON output in the prompt; use response_format={"type": "json_object"} where the selected model supports it.
Handle Groq rate limits (429) with exponential backoff before falling back to heuristic ranking.
Log model ID and latency per request; Groq responses include token usage in response.usage.

3.5 Output Display Layer
Responsibility: Render recommendations in a clear, scannable format.
Component
Role
RecommendationPresenter
Formats RecommendationResponse for UI or CLI.
ResultsView
Cards/table showing name, cuisine, rating, cost, explanation.
SummaryBanner
Optional LLM summary at the top.

Display requirements (from context):
Each result card/row must show:
Restaurant Name
Cuisine
Rating
Estimated Cost
AI-generated explanation
UX considerations:
Show applied filters (location, budget, etc.) above results.
Display "no results" state with suggestions to broaden filters.
Show loading state while dataset loads / LLM responds.
Rank badge (1, 2, 3…) for quick scanning.

4. Request Flow (Sequence Diagram)
Recommendation ServiceGroq ClientPrompt BuilderRestaurant FilterRestaurant RepositoryPreference ValidatorAPI ControllerPresentation LayerRecommendation ServiceGroq ClientPrompt BuilderRestaurant FilterRestaurant RepositoryPreference ValidatorAPI ControllerPresentation LayerUserEnter preferencesPOST /recommendvalidate(preferences)UserPreferencesget_all() / queryrestaurants[]filter(restaurants, preferences)candidates[]build(preferences, candidates)promptrecommend(prompt, candidates)complete(prompt)JSON responseparse & enrichRecommendationResponseJSONRender ranked cardsUser

5. Proposed Module Structure
Recommended layout for a Python implementation:
zomato-milestone1/
├── docs/
│   ├── context.md
│   ├── architecture.md
│   └── problemStatement.txt
├── src/
│   ├── __init__.py
│   ├── main.py                    # entry point (CLI or app bootstrap)
│   ├── config.py                  # env vars, budget thresholds, top-K
│   ├── models/
│   │   ├── restaurant.py          # Restaurant dataclass
│   │   ├── preferences.py         # UserPreferences dataclass
│   │   └── recommendation.py      # Recommendation, RecommendationResponse
│   ├── data/
│   │   ├── loader.py              # Hugging Face dataset loader
│   │   ├── preprocessor.py        # normalization & schema mapping
│   │   └── repository.py          # in-memory query interface
│   ├── services/
│   │   ├── filter.py              # RestaurantFilter
│   │   ├── prompt_builder.py      # PromptBuilder
│   │   ├── llm_client.py          # Groq API adapter
│   │   └── recommendation.py      # RecommendationService orchestrator
│   ├── api/
│   │   ├── routes.py              # FastAPI routes (optional)
│   │   └── schemas.py             # request/response Pydantic models
│   └── ui/
│       ├── cli.py                 # terminal interface
│       └── streamlit_app.py       # or Gradio web UI (optional)
├── tests/
│   ├── test_filter.py
│   ├── test_preprocessor.py
│   └── test_recommendation.py
├── data/                          # cached parquet/csv (gitignored)
├── .env.example                   # GROQ_API_KEY and model config
├── requirements.txt
└── README.md


6. Technology Stack (Recommended)
Layer
Technology
Rationale
Language
Python 3.11+
Strong ecosystem for data + LLM integration.
Dataset
datasets (Hugging Face)
Direct access to the specified dataset.
Data processing
pandas
Filtering, normalization, caching.
LLM
Groq (llama-3.3-70b-versatile)
Fast, low-latency inference for ranking + explanation tasks.
LLM SDK
groq
Official Groq Python client for chat completions.
API (optional)
FastAPI
Lightweight async REST for frontend decoupling.
UI (optional)
Streamlit or Gradio
Rapid prototyping of preference form + results.
Config
pydantic-settings + .env
Typed config and secret management.
Testing
pytest
Unit tests for filter, parser, preprocessor.


7. API Design (Optional REST Layer)
If exposing a backend API:
POST /api/v1/recommend
Request:
{
  "location": "Bangalore",
  "budget": "medium",
  "cuisine": "Italian",
  "min_rating": 4.0,
  "additional": "family-friendly, outdoor seating"
}

Response:
{
  "summary": "Based on your preference for Italian cuisine in Bangalore with a medium budget...",
  "recommendations": [
    {
      "rank": 1,
      "name": "Example Ristorante",
      "cuisine": "Italian, Continental",
      "rating": 4.5,
      "estimated_cost": 1200,
      "explanation": "Highly rated Italian spot within your budget, known for family-friendly ambiance."
    }
  ],
  "metadata": {
    "candidates_considered": 18,
    "filters_applied": {
      "location": "Bangalore",
      "budget": "medium",
      "min_rating": 4.0,
      "cuisine": "Italian"
    },
    "model": "llama-3.3-70b-versatile"
  }
}

GET /api/v1/health
Returns service status and whether the dataset is loaded.
GET /api/v1/locations
Returns distinct locations from the dataset (populates UI dropdowns).
GET /api/v1/cuisines
Returns distinct cuisines extracted from the dataset.

8. Data Flow Summary
Hugging Face Dataset
        │
        ▼
  [Load & Preprocess] ──► RestaurantRepository (cached)
                                │
User Preferences ──► [Validate] ──► [Filter candidates]
                                          │
                                          ▼
                                   [Build LLM Prompt]
                                          │
                                          ▼
                                    [LLM Rank + Explain]
                                          │
                                          ▼
                                   [Parse & Enrich]
                                          │
                                          ▼
                              RecommendationResponse ──► UI


9. Cross-Cutting Concerns
9.1 Configuration
Centralize in config.py:
HF_DATASET_NAME
BUDGET_THRESHOLDS
MAX_CANDIDATES_FOR_LLM
TOP_K_RECOMMENDATIONS
GROQ_MODEL (default: llama-3.3-70b-versatile)
GROQ_API_KEY
GROQ_TEMPERATURE
DATA_CACHE_PATH
9.2 Error Handling
Scenario
Behavior
Dataset download fails
Retry with backoff; show clear error in UI.
No restaurants match filters
Relax constraints or prompt user to adjust input.
LLM returns invalid JSON
Retry once; fallback to heuristic ranking.
LLM timeout / Groq 429 rate limit
Retry with backoff; then return heuristic top-K with note that AI explanation is unavailable.
Unknown location
Suggest valid locations from dataset.

9.3 Logging & Observability
Log filter counts (input size → candidate size).
Log LLM latency and token usage.
Do not log full prompts containing API keys.
Optional: trace ID per recommendation request.
9.4 Security
Store API keys in environment variables, never in source control.
Validate and sanitize all user inputs.
Rate-limit API endpoints if deployed publicly.

10. Deployment Topology
Development (local):
Developer Machine
├── Python app (Streamlit / FastAPI + CLI)
├── Cached dataset in ./data/
└── Groq API (cloud)

Minimal production:
User
Streamlit / Static Frontend
FastAPI Backend
Dataset Cache
Groq API
Pre-load dataset at container startup.
Single-stateless API instance is sufficient for milestone scope.
Scale horizontally later by sharing a read-only dataset snapshot.

11. Testing Strategy
Test type
Scope
Example
Unit
RestaurantFilter
Location + budget + rating filters return expected subset.
Unit
Preprocessor
Cuisine string parsing, numeric coercion.
Unit
ResponseParser
Valid/invalid LLM JSON handling.
Integration
RecommendationService
Mock LLM returns fixed JSON; verify enriched output.
Snapshot
PromptBuilder
Prompt contains all candidates and preference fields.

Use a frozen subset of the dataset (10–20 rows) in test fixtures for deterministic tests.

12. Implementation Phases
Phase
Deliverable
Phase 1 — Data
Load Hugging Face dataset, preprocess, cache, expose repository.
Phase 2 — Filter
Implement preference validation and deterministic filtering.
Phase 3 — LLM
Prompt builder, LLM client, response parser, enricher.
Phase 4 — UI
CLI or Streamlit form + results display.
Phase 5 — Hardening
Error handling, fallback ranking, tests, README.


13. Architecture Decisions
Decision
Choice
Alternatives considered
LLM provider
Groq (llama-3.3-70b-versatile)
OpenAI, Anthropic, local models
Pre-filter before LLM
Yes — hard filters in code
Let LLM filter entire dataset (expensive, unreliable)
LLM output format
Structured JSON
Free-form text (harder to parse)
Data storage
In-memory DataFrame
Database (unnecessary for read-only milestone dataset)
Ranking split
Heuristic shortlist + LLM final rank
Pure LLM or pure heuristic
UI approach
Streamlit for speed
React SPA (more effort for milestone 1)


14. Related Documents
context.md — product requirements and workflow
problemStatement.txt — original problem statement

