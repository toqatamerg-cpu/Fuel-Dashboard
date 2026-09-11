# Fuel Theft Analytics Dashboard

Interactive Dash dashboard for analyzing fuel station theft data.

## Files
- `dashboard.py` — main Dash app
- `cleaned_fuel_data.csv` — data used by the dashboard
- `Fuel_station_theft_dataset.csv` — raw dataset
- `cleaned_data.ipynb` — data cleaning / analysis notebook
- `fuel_theft_model.pkl` — trained model (not loaded by the dashboard itself)
- `requirements.txt`, `Procfile` — needed for Render/Railway deployment
- `api/index.py`, `vercel.json` — needed for Vercel deployment

## Run locally
```bash
pip install -r requirements.txt
python dashboard.py
```
Then open http://127.0.0.1:8050

## Deploy so anyone can open it with a link
GitHub only stores the code — it does not run Python apps for you. To get a
live link people can open and interact with, deploy the repo on a free host
like **Render**:

1. Push this folder to GitHub (see steps below).
2. Go to https://render.com → sign up with your GitHub account.
3. **New +** → **Web Service** → pick this repository.
4. Settings:
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn dashboard:server`
5. Click **Create Web Service**. After the build finishes, Render gives you a
   public URL like `https://your-app.onrender.com` — that's the link you
   share. (Free tier sleeps after inactivity and wakes up on the next visit,
   which takes ~30–50 seconds.)

Railway (railway.app) works the same way and also reads `Procfile`.

## Deploy on Vercel instead
This repo also includes `api/index.py` and `vercel.json`, ready for Vercel's
Python (serverless) runtime.

1. Push this repo to GitHub (steps below).
2. Go to https://vercel.com → **Add New** → **Project** → import this repo.
3. Vercel auto-detects `vercel.json` — no extra config needed. Click **Deploy**.
4. You'll get a URL like `https://your-app.vercel.app` — that's the shareable link.

Notes on the Vercel path (differences from Render/Railway):
- Vercel runs the app as a **serverless function**, not a persistent server —
  each request may cold-start, and there's a free-tier execution time limit
  per request (a few seconds), so very heavy callbacks could time out.
- The CSV is small (~35 KB) so re-reading it per invocation is not an issue
  here.
- If you ever add authentication, sessions, or large in-memory caches to the
  dashboard, those won't persist between invocations on Vercel — Render/
  Railway don't have that limitation since they run one long-lived process.
