# Edge Cases & Corner Scenarios

This document outlines the known corner scenarios and edge cases for the Zomato AI-Powered Restaurant Recommendation System. Handling these gracefully ensures a robust and reliable user experience.

---

## 1. Data Ingestion & Preprocessing

| Edge Case | Scenario | Expected Behavior |
|-----------|----------|-------------------|
| **HF Download Failure** | Hugging Face is down or network connection drops. | Retry 3 times with exponential backoff (1s, 2s, 4s). If all fail, display a clear "Dataset Unavailable" error in UI and exit gracefully. |
| **Malformed Cost/Rating** | A restaurant row has a rating like "NEW" or a cost like `NaN`. | Exclude the row during preprocessing. Only restaurants with valid, parsable numerics for critical fields are loaded. |
| **Empty or NaN Cuisine** | A restaurant lacks cuisine data (`NaN` or empty string). | Parse as an empty list `[]`. The restaurant will be excluded if the user specifically requests a cuisine, but included if cuisine is left blank. |
| **Zero/Negative Cost** | `cost_for_two` evaluates to `0` or a negative number. | Drop the row during preprocessing to avoid breaking the budget tier logic. |
| **Messy Location Strings** | Locations have trailing spaces or mixed casing (e.g., `  bangalore `). | Trim whitespace, title-case the string, and apply an alias map (e.g., `Bengaluru` → `Bangalore`) to ensure exact matching works reliably. |

---

## 2. Filtering & Validation

| Edge Case | Scenario | Expected Behavior |
|-----------|----------|-------------------|
| **Unknown Location Input** | User searches for a city not in the dataset (e.g., "New York"). | Return a `ValidationError` / 400 Bad Request. The UI should suggest the closest valid locations from the dataset. |
| **Excessively Long Preferences** | The `additional` free-text input exceeds 500 characters. | Truncate the text at 500 characters and log a warning to prevent excessive prompt token usage and potential prompt injection. |
| **Overly Strict Filters** | Location, budget, and high rating combined result in 0 candidates. | Trigger the constraint relaxation pipeline. Relax `cuisine` first, then `budget`, then `min_rating`. Surface a warning in the UI: "Expanded filters to find results." |
| **Zero Candidates After Relaxation** | Even after relaxing all constraints, no restaurants are found for the location. | Return an empty state response. Display "No results found" in the UI with suggestions to select a different location.  |

---

## 3. LLM Integration (Groq)

| Edge Case | Scenario | Expected Behavior |
|-----------|----------|-------------------|
| **Invalid JSON Output** | Groq returns markdown or malformed JSON instead of a valid object. | Catch the `ParseError`. Retry the exact prompt once with `temperature=0.1` for strict determinism. If it fails again, use heuristic fallback ranking. |
| **Hallucinated IDs** | Groq recommends a restaurant `id` that was not in the candidate list. | The `ResponseParser` must reject the output and throw a `ParseError`. Trigger a retry, then fallback if needed. |
| **Duplicate IDs** | Groq returns the same restaurant ID multiple times in the ranking. | Deduplicate the list during parsing, keeping only the first occurrence. |
| **Excess Recommendations** | Groq returns 7 recommendations when `top_k=5` was requested. | Truncate the parsed recommendations array to `top_k` before enriching. |
| **Fewer Recommendations** | Groq returns 3 recommendations when `top_k=5` was requested. | Accept the 3 recommendations. The UI must gracefully handle displaying fewer cards than requested. |
| **Groq 429 Rate Limit** | Too many requests hit the Groq API concurrently. | Catch the 429 error, apply exponential backoff, and retry up to 3 times. |
| **Groq 503 / Timeout** | The primary `llama-3.3-70b-versatile` model is down or timing out. | Catch the timeout, switch to `GROQ_FALLBACK_MODEL` (`llama-3.1-8b-instant`), and retry. If both fail, use heuristic fallback ranking. |

---

## 4. UI & Concurrency

| Edge Case | Scenario | Expected Behavior |
|-----------|----------|-------------------|
| **Concurrent API Requests** | Multiple users hit `/recommend` simultaneously. | Each request creates its own ephemeral filter and prompt pipeline. The repository is a thread-safe read-only singleton. |
| **Fallback Ranking Display** | Groq is completely unavailable; system falls back to heuristic ranking. | UI must display the results but prominently show a banner: "⚠️ AI explanations unavailable — showing top-rated results based on your filters." |
| **Missing AI Summary** | LLM response omits the `summary` key but includes recommendations. | Handle gracefully: set `summary = None` and omit the summary banner in the UI without crashing the app. |
