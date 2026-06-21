# Zomato AI Recommender

Zomato AI Recommender is an intelligent web application built to help users discover the best restaurant options based on their preferences. It utilizes the **Groq API** to process user inputs (like budget, location, and rating) and provide tailored, human-readable restaurant recommendations.

## Features

- **AI-Powered Recommendations:** Get detailed explanations on why a specific restaurant was recommended using Groq API's blazing fast LLM.
- **Smart Filtering:** Filters restaurants by location, cuisine, budget (low/medium/high), and minimum rating.
- **Robust Fallback Mechanism:** In the event of an AI service outage, the app seamlessly falls back to a heuristic ranking algorithm to ensure users always receive recommendations.
- **Deduplication System:** Automatically handles data inconsistencies and guarantees only unique restaurants appear in the final output.
- **Modern Interface:** A sleek and simple frontend served directly via FastAPI.

## Tech Stack

- **Backend:** Python 3, FastAPI, Uvicorn, Pydantic, Pandas
- **AI/LLM:** Groq API (via `groq` python SDK)
- **Frontend:** HTML, CSS, JavaScript
- **Testing:** Pytest

## Project Structure

```text
.
├── data/                 # Raw datasets and processed files
├── frontend/             # Static UI assets (HTML, JS, CSS)
├── src/
│   ├── api/              # FastAPI routers and schemas
│   ├── data/             # Data loading and preprocessing pipelines
│   ├── models/           # Pydantic models (UserPreferences, Restaurant, etc.)
│   └── services/         # Core business logic (Filtering, Prompts, Groq API, Enricher)
├── tests/                # Pytest suites
├── requirements.txt      # Project dependencies
├── run_prediction.py     # CLI script to test recommendations
└── main.py               # Main FastAPI application entry point
```

## Getting Started

### Prerequisites

- Python 3.9+
- A [Groq API Key](https://console.groq.com/) for AI generation.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sibaniacharya/zomato-ai-milestone.git
   cd zomato-ai-milestone
   ```

2. **Create and activate a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration:**
   Copy the `.env.example` to `.env` and add your Groq API key:
   ```bash
   cp .env.example .env
   ```
   Open `.env` and set `GROQ_API_KEY=your_api_key_here`.

### Running the Application

To start the FastAPI web server, run:

```bash
uvicorn src.main:app --reload
```

Then, open your web browser and navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000) to access the interactive web interface!

## Testing

To run the automated test suite, use:
```bash
pytest tests/
```