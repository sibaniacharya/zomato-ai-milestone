# Project Context: AI-Powered Restaurant Recommendation System

> Zomato-inspired restaurant recommendation service combining structured restaurant data with LLM-powered personalization and explainability.

---

## 1. Problem Overview

Build an **AI-powered restaurant recommendation service** inspired by Zomato. The system intelligently suggests restaurants based on user preferences by combining **structured data** with a **Large Language Model (LLM)**.

### Objective

Design and implement an application that:

- Takes user preferences (location, budget, cuisine, ratings, and more)
- Uses a real-world dataset of restaurants
- Leverages an LLM to generate personalized, human-like recommendations
- Displays clear and useful results to the user

---

## 2. System Workflow

### 2.1 Data Ingestion

- Load and preprocess the Zomato dataset from Hugging Face:
  - **Dataset URL:** [ManikaSaini/zomato-restaurant-recommendation](https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation)
- Extract relevant fields such as:
  - Restaurant name
  - Location
  - Cuisine
  - Cost
  - Rating
  - Other useful metadata (votes, restaurant type, etc.)

### 2.2 User Input

Collect user preferences:

| Field | Description | Example |
|-------|-------------|---------|
| **Location** | City or locality | Delhi, Bangalore |
| **Budget** | Spending tier | low, medium, high |
| **Cuisine** | Preferred cuisine type | Italian, Chinese |
| **Minimum rating** | Lowest acceptable rating | 3.5, 4.0 |
| **Additional preferences** | Free-text soft signals | family-friendly, quick service |

### 2.3 Integration Layer

- Filter and prepare relevant restaurant data based on user input
- Pass structured results into an LLM prompt
- Design a prompt that helps the LLM reason and rank options

### 2.4 Recommendation Engine

Use the LLM to:

- Rank restaurants
- Provide explanations (why each recommendation fits the user)
- Optionally summarize the overall choice set

### 2.5 Output Display

Present top recommendations in a user-friendly format. Each result must include:

1. **Restaurant Name**
2. **Cuisine**
3. **Rating**
4. **Estimated Cost**
5. **AI-generated explanation**

---

## 3. Data Model

### 3.1 Canonical Restaurant Schema

```python
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
```

### 3.2 Preprocessing Requirements

1. Download dataset split (typically `train`)
2. Select and rename relevant columns to the canonical schema
3. Parse cuisine strings into lists (e.g. `"Italian, Chinese"` → `["Italian", "Chinese"]`)
4. Coerce rating and cost to numeric types; drop or impute invalid rows
5. Normalize location strings (trim, title-case, alias map for city names)
6. Derive `budget_tier` from `cost_for_two` using configurable thresholds

### 3.3 Budget Tier Thresholds

| Tier | Typical `cost_for_two` range (INR) |
|------|-------------------------------------|
| **low** | ≤ 500 |
| **medium** | 501 – 1500 |
| **high** | > 1500 |

> Thresholds should be tuned after inspecting the actual dataset distribution.

### 3.4 Caching Strategy

- Load once into a pandas DataFrame or list of `Restaurant` objects
- Persist a local parquet/CSV snapshot to avoid repeated Hugging Face downloads during development

---

## 4. User Preferences Model

```python
UserPreferences = {
    "location": str,           # required
    "budget": str,             # "low" | "medium" | "high"
    "cuisine": str | None,     # optional primary cuisine
    "min_rating": float,       # e.g. 3.5
    "additional": str | None,  # free-text: "family-friendly, quick service"
}
```

### Validation Rules

| Field | Rule |
|-------|------|
| **location** | Non-empty; must match at least one value in the dataset (or suggest closest matches) |
| **budget** | One of `low`, `medium`, `high` |
| **min_rating** | Float in `[0.0, 5.0]` |
| **cuisine** | Optional; fuzzy match against known cuisine vocabulary extracted from dataset |
| **additional** | Optional free text passed through to the LLM for soft matching |

---

## 5. Filtering & Integration Logic

### 5.1 Deterministic Filter Pipeline

Apply hard filters **before** the LLM to reduce token cost and hallucination risk:

```
all restaurants
  → filter by location (exact or case-insensitive match)
  → filter by budget tier
  → filter by min_rating
  → filter by cuisine (if provided; match if cuisine in restaurant.cuisines)
  → sort by rating desc, then votes desc
  → take top N candidates (default N = 15–20)
```

### 5.2 Constraint Relaxation

If zero candidates remain, relax constraints in order:

1. cuisine
2. budget
3. min_rating

Surface a warning to the user when constraints are relaxed.

### 5.3 LLM Prompt Requirements

The prompt must include:

1. **System instructions** — role, output format (JSON), ranking criteria
2. **User preferences** — serialized `UserPreferences`
3. **Candidate restaurants** — compact JSON array of filtered restaurants
4. **Task** — rank top K (e.g. 5), explain each pick, optionally summarize

**Design principles:**

- Require JSON output from the LLM for reliable parsing
- Include restaurant `id` in candidates so explanations map back to structured data
- Instruct the model to **only recommend from the provided list** (no fabrication)
- Pass additional preferences as soft signals the LLM may use in ranking/explanation

**Example expected LLM output shape:**

```json
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
```

---

## 6. Recommendation Output Model

```python
Recommendation = {
    "rank": int,
    "name": str,
    "cuisine": str,           # joined cuisine string for display
    "rating": float,
    "estimated_cost": int,      # cost_for_two
    "explanation": str,         # LLM-generated
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
```

### Reliability Patterns

| Pattern | Purpose |
|---------|---------|
| Structured output / JSON mode | Reduce parse failures |
| Retry with temperature reduction | Recover from invalid JSON |
| Fallback ranking | If LLM fails, return heuristic top-K by rating with a generic explanation |
| Idempotency | Same preferences + same dataset snapshot → reproducible candidate set |

### What the LLM Is NOT Used For

- Loading data
- Hard filtering by location/budget/rating
- Inventing restaurants not in the candidate list

---

## 7. LLM Provider: Groq

Groq is the **sole LLM provider** for this project.

| Setting | Default | Notes |
|---------|---------|-------|
| SDK | `groq` | Official Python client (`pip install groq`) |
| API key | `GROQ_API_KEY` | Required; set in `.env`, never committed |
| Model | `llama-3.3-70b-versatile` | Strong reasoning for ranking and explanations |
| Fallback model | `llama-3.1-8b-instant` | Optional faster/cheaper alternative for dev |
| Temperature | `0.3` | Low enough for consistent JSON; retry with `0.1` on parse failure |

**Groq-specific considerations:**

- Very low latency inference — suitable for interactive UI feedback
- Enforce JSON output in the prompt; use `response_format={"type": "json_object"}` where supported
- Handle Groq rate limits (429) with exponential backoff before falling back to heuristic ranking
- Log model ID and latency per request; Groq responses include token usage in `response.usage`

---

## 8. Output Display Requirements

### Required Fields Per Result

Each result card/row must show:

1. Restaurant Name
2. Cuisine
3. Rating
4. Estimated Cost
5. AI-generated explanation

### UX Considerations

- Show applied filters (location, budget, etc.) above results
- Display "no results" state with suggestions to broaden filters
- Show loading state while dataset loads / LLM responds
- Rank badge (1, 2, 3…) for quick scanning
- Optional LLM summary banner at the top

---

## 9. Architecture Goals

| Goal | Description |
|------|-------------|
| **Separation of concerns** | Data loading, filtering, LLM reasoning, and presentation are isolated modules with clear interfaces |
| **Deterministic pre-filtering** | Hard constraints (location, budget, rating) are applied before the LLM |
| **Explainability** | Every recommendation includes an LLM-generated rationale tied to user preferences |
| **Extensibility** | Swap UI frameworks or data sources without rewriting core logic; LLM access isolated behind a Groq adapter |
| **Testability** | Pure functions for filtering/ranking prep; mockable LLM adapter for unit tests |

---

## 10. Technology Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| Language | Python 3.11+ | Strong ecosystem for data + LLM integration |
| Dataset | `datasets` (Hugging Face) | Direct access to the specified dataset |
| Data processing | pandas | Filtering, normalization, caching |
| LLM | Groq (`llama-3.3-70b-versatile`) | Fast, low-latency inference for ranking + explanation |
| LLM SDK | `groq` | Official Groq Python client |
| API (optional) | FastAPI | Lightweight async REST for frontend decoupling |
| UI (optional) | Streamlit or Gradio | Rapid prototyping of preference form + results |
| Config | pydantic-settings + `.env` | Typed config and secret management |
| Testing | pytest | Unit tests for filter, parser, preprocessor |

---

## 11. Proposed Module Structure

```
zomato-milestone1/
├── docs/
│   ├── context.md
│   ├── architecture.md
│   ├── implementation-plan.md
│   ├── edge-case.md
│   └── problemStatement.txt
├── src/
│   ├── __init__.py
│   ├── main.py                  # entry point (CLI or app bootstrap)
│   ├── config.py                # env vars, budget thresholds, top-K
│   ├── models/
│   │   ├── restaurant.py        # Restaurant dataclass
│   │   ├── preferences.py       # UserPreferences dataclass
│   │   └── recommendation.py    # Recommendation, RecommendationResponse
│   ├── data/
│   │   ├── loader.py            # Hugging Face dataset loader
│   │   ├── preprocessor.py      # normalization & schema mapping
│   │   └── repository.py        # in-memory query interface
│   ├── services/
│   │   ├── filter.py            # RestaurantFilter
│   │   ├── prompt_builder.py    # PromptBuilder
│   │   ├── llm_client.py        # Groq API adapter
│   │   └── recommendation.py    # RecommendationService orchestrator
│   ├── api/
│   │   ├── routes.py            # FastAPI routes (optional)
│   │   └── schemas.py           # request/response Pydantic models
│   └── ui/
│       ├── cli.py               # terminal interface
│       └── streamlit_app.py     # or Gradio web UI (optional)
├── tests/
│   ├── test_filter.py
│   ├── test_preprocessor.py
│   └── test_recommendation.py
├── data/                        # cached parquet/csv (gitignored)
├── .env.example                 # GROQ_API_KEY and model config
├── requirements.txt
└── README.md
```

---

## 12. API Design (Optional REST Layer)

### `POST /api/v1/recommend`

**Request:**

```json
{
  "location": "Bangalore",
  "budget": "medium",
  "cuisine": "Italian",
  "min_rating": 4.0,
  "additional": "family-friendly, outdoor seating"
}
```

**Response:**

```json
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
```

### Additional Endpoints

| Endpoint | Purpose |
|----------|---------|
| `GET /api/v1/health` | Service status and whether the dataset is loaded |
| `GET /api/v1/locations` | Distinct locations from the dataset (populates UI dropdowns) |
| `GET /api/v1/cuisines` | Distinct cuisines extracted from the dataset |

---

## 13. Data Flow Summary

```
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
[LLM Rank + Explain]  (Groq)
        │
        ▼
[Parse & Enrich]
        │
        ▼
RecommendationResponse ──► UI
```

---

## 14. Configuration

Centralize in `config.py`:

| Variable | Purpose |
|----------|---------|
| `HF_DATASET_NAME` | Hugging Face dataset identifier |
| `BUDGET_THRESHOLDS` | low/medium/high cost boundaries |
| `MAX_CANDIDATES_FOR_LLM` | Cap on candidates sent to LLM (default 15–20) |
| `TOP_K_RECOMMENDATIONS` | Number of final recommendations (default 5) |
| `GROQ_MODEL` | Default: `llama-3.3-70b-versatile` |
| `GROQ_API_KEY` | Groq API key from environment |
| `GROQ_TEMPERATURE` | Default: `0.3` |
| `DATA_CACHE_PATH` | Local cache path for preprocessed dataset |

---

## 15. Error Handling

| Scenario | Behavior |
|----------|----------|
| Dataset download fails | Retry with backoff; show clear error in UI |
| No restaurants match filters | Relax constraints or prompt user to adjust input |
| LLM returns invalid JSON | Retry once; fallback to heuristic ranking |
| LLM timeout / Groq 429 rate limit | Retry with backoff; then return heuristic top-K with note that AI explanation is unavailable |
| Unknown location | Suggest valid locations from dataset |

---

## 16. Security & Observability

### Security

- Store API keys in environment variables, never in source control
- Validate and sanitize all user inputs
- Rate-limit API endpoints if deployed publicly

### Logging

- Log filter counts (input size → candidate size)
- Log LLM latency and token usage
- Do **not** log full prompts containing API keys
- Optional: trace ID per recommendation request

---

## 17. Implementation Phases

| Phase | Deliverable |
|-------|-------------|
| **Phase 0** | Project setup, docs, environment configuration |
| **Phase 1 — Data Load** | Hugging Face dataset, preprocess, cache, expose repository |
| **Phase 2 — Filter** | Preference validation and deterministic filtering |
| **Phase 3 — LLM** | Prompt builder, LLM client, response parser, enricher |
| **Phase 4 — UI** | CLI or Streamlit form + results display |
| **Phase 5 — Hardening** | Error handling, fallback ranking, tests, README |

---

## 18. Key Architecture Decisions

| Decision | Choice | Alternatives Considered |
|----------|--------|-------------------------|
| LLM provider | Groq (`llama-3.3-70b-versatile`) | OpenAI, Anthropic, local models |
| Pre-filter before LLM | Yes — hard filters in code | Let LLM filter entire dataset (expensive, unreliable) |
| LLM output format | Structured JSON | Free-form text (harder to parse) |
| Data storage | In-memory DataFrame | Database (unnecessary for read-only milestone dataset) |
| Ranking split | Heuristic shortlist + LLM final rank | Pure LLM or pure heuristic |
| UI approach | Streamlit for speed | React SPA (more effort for milestone 1) |

---

## 19. Testing Strategy

| Test Type | Scope | Example |
|-----------|-------|---------|
| Unit | RestaurantFilter | Location + budget + rating filters return expected subset |
| Unit | Preprocessor | Cuisine string parsing, numeric coercion |
| Unit | ResponseParser | Valid/invalid LLM JSON handling |
| Integration | RecommendationService | Mock LLM returns fixed JSON; verify enriched output |
| Snapshot | PromptBuilder | Prompt contains all candidates and preference fields |

Use a frozen subset of the dataset (10–20 rows) in test fixtures for deterministic tests.

---

## 20. Documentation Structure

This project uses a docs-driven development workflow:

| File | Purpose |
|------|---------|
| `problemStatement.txt` | Basic problem statement of the project |
| `context.md` | Stores the necessary context of the project (this document) |
| `architecture.md` | Detailed technical architecture description |
| `implementation-plan.md` | Phase-wise implementation plan |
| `edge-case.md` | Corner scenarios (living document) |

### Recommended Workflow

1. Generate `context.md` from `problemStatement.txt`
2. Generate detailed `architecture.md` using `context.md`
3. Confirm LLM provider is Groq in `architecture.md`
4. Generate phase-wise `implementation-plan.md` using `architecture.md` and `context.md`
5. Generate `edge-case.md` for corner scenarios
6. Implement Phase 0 as per `implementation-plan.md`

---

## 21. AI Tools Reference

Tools used during development:

- [Cursor](https://cursor.com/download)
- [Antigravity IDE](https://antigravity.google/product/antigravity-ide) (PRO – JIO SIM) — use Pro model or Claude Opus for generating context files
- [Qoder](https://qoder.com/)

### Developer Notes

- Preview any Markdown file: `Ctrl + Shift + V` (Windows) / `Cmd + Shift + V` (Mac)
- Reference files in prompts using `@filename`
- Use **Mermaid** extension for diagrams

---

## 22. Related Documents

| Document | Description |
|----------|-------------|
| [problemStatement.txt](./problemStatement.txt) | Original problem statement |
| [architecture.md](./architecture.md) | Detailed technical architecture (to be generated) |
| [implementation-plan.md](./implementation-plan.md) | Phase-wise build plan (to be generated) |
| [edge-case.md](./edge-case.md) | Corner scenarios and edge cases (to be generated) |
