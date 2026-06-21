# Deployment Plan

This document outlines the step-by-step strategy for deploying the Zomato AI Recommender project, specifically splitting the architecture to host the **Backend on Railway** and the **Frontend on Vercel**.

## 1. Prerequisites
- A GitHub account with the project repository pushed and up-to-date.
- A [Railway account](https://railway.app/).
- A [Vercel account](https://vercel.com/).
- Your Groq API Key.

---

## 2. Backend Deployment (Railway)

We will deploy the FastAPI Python backend to Railway, which will automatically detect the Python environment from `requirements.txt`.

### Steps:
1. **Login to Railway:** Go to [Railway.app](https://railway.app/) and click **New Project** -> **Deploy from GitHub repo**.
2. **Select Repository:** Choose your `zomato-ai-milestone` repository.
3. **Configure Environment Variables:**
   - Go to the **Variables** tab of your new service.
   - Add a new variable:
     - `GROQ_API_KEY` = `your_groq_api_key_here`
4. **Custom Start Command:**
   - Go to the **Settings** tab.
   - Under **Deploy**, find the **Custom Start Command** (or add a `Procfile` to the repo). 
   - Set the start command to:
     ```bash
     uvicorn src.main:app --host 0.0.0.0 --port $PORT
     ```
5. **Generate Domain:**
   - In the **Settings** tab, go to **Networking**.
   - Click **Generate Domain**.
   - Note down this URL (e.g., `https://zomato-backend-production.up.railway.app`). You will need it for the frontend.

---

## 3. Frontend Deployment (Vercel)

The frontend consists of static HTML, CSS, and vanilla JS. Since the API will now live on a different domain (Railway), we will use a `vercel.json` rewrite to proxy API requests to the backend. This prevents CORS issues and keeps the code clean without hardcoding URLs in the JavaScript.

### Preparation Step (Local)
Create a `vercel.json` file inside your `frontend/` directory with the following content. **Replace `YOUR_RAILWAY_URL`** with the domain you got in Step 2:

```json
{
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://YOUR_RAILWAY_URL/api/:path*"
    }
  ]
}
```

Commit and push this change to GitHub:
```bash
git add frontend/vercel.json
git commit -m "Add Vercel API rewrites"
git push
```

### Steps:
1. **Login to Vercel:** Go to [Vercel.com](https://vercel.com/) and click **Add New** -> **Project**.
2. **Import Repository:** Import the `zomato-ai-milestone` repository from GitHub.
3. **Configure Project:**
   - **Framework Preset:** Other
   - **Root Directory:** Edit this and select the `frontend` folder. *(This is crucial so Vercel only serves the UI files)*
   - Leave Build Command and Output Directory empty/default.
4. **Deploy:** Click **Deploy**. Vercel will process the static files and the `vercel.json` rewrite configuration.

---

## 4. Post-Deployment Verification

1. Go to the Vercel-provided URL (e.g., `https://zomato-ai.vercel.app`).
2. Verify that the dropdowns for Location and Cuisine successfully populate. This confirms that the Vercel API proxy is successfully reaching the Railway backend.
3. Submit a preference query and verify that the AI explanations load correctly. This confirms the Railway backend is successfully communicating with the Groq API.
