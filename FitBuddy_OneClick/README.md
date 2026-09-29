# FitBuddy AI — One-Click Windows Version

## Run it

1. Install **Python 3.10 or newer** from https://www.python.org/downloads/ if it is not already installed.
2. Double-click **`run.bat`**.
3. The first run creates a local `.venv` folder and installs the required packages.
4. Your browser opens automatically at `http://127.0.0.1:8000`.

After the first setup, future runs are much faster.

## Important

Do **not** double-click `app/static/index.html`. The site is designed to run through FastAPI so that `/style.css`, `/app.js`, and `/api/...` resolve correctly.

## Optional Gemini AI

The app works without an API key using its built-in fallback planner.

For Gemini-generated plans:

1. Copy `.env.example` to `.env`.
2. Put your key in `GEMINI_API_KEY`.
3. Run `run.bat` again.

Example `.env`:

```env
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash
```

## Stop the app

Close the small **FitBuddy Server** command window.

## Troubleshooting

If port 8000 is already in use, stop the other app using it and run `run.bat` again.
