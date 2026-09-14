# JAY Job AI

Personal AI job-search command center for real opportunities, resume matching, application preparation and interview preparation.

## Public website

The `frontend/` directory is deployed with GitHub Pages by `.github/workflows/pages.yml`.

## Agent features

- PDF/DOCX resume parsing
- Greenhouse public job discovery
- Lever public job discovery
- Company career-page discovery
- HR-focused filtering for Bengaluru, Mysuru, Coimbatore, Kerala and remote roles
- AI 0–100 job-fit scoring
- Truthful tailored application preparation
- Interview preparation
- SQLite tracking
- Playwright application-page inspection/review

## Windows backend setup

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install chromium
Copy-Item .env.example .env
```

Add your OpenAI API key to `.env` locally. **Never commit the key to GitHub.**

Configure real public job sources in `config/sources.yaml`, then run:

```powershell
uvicorn backend.main:app --reload --port 8000
```

For production, deploy the backend separately and use HTTPS. The public frontend must never contain your OpenAI API key.

## Application safety

The agent discovers jobs, scores them, drafts truthful application content and can inspect application pages. Final submission remains a user-approved action. It must not fabricate experience, education, work authorization, salary history or other candidate facts.
