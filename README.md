# AI DevOps Platform

Full-stack prototype for an AI-assisted DevOps workspace with:

- Dashboard
- Jira Workspace
- GitHub Workspace
- Pipeline Runs
- Pull Requests
- GitHub Actions
- AI Assistant
- Reports & Analytics
- Settings & Integrations

## Stack

- **Backend:** FastAPI
- **Frontend:** React + TypeScript + Vite + Recharts
- **Data source:** mock in-memory project data exposed through REST endpoints

## Project layout

```text
backend/
  main.py                 # FastAPI app with all API endpoints
  user_service.py         # registration service used by tests
  services/               # compatibility wrappers for tests/imports
  utils/                  # compatibility wrappers for tests/imports
frontend/
  package.json
  index.html
  src/
    App.tsx               # multi-page app shell and screens
    components/ui.tsx     # shared cards/badges/sections
    lib/api.ts            # API client
    lib/types.ts          # shared types
```

## Backend routes

- `GET /api/dashboard`
- `GET /api/jira`
- `GET /api/jira/{ticket_key}`
- `POST /api/jira/tickets`
- `POST /api/jira/{ticket_key}/sync`
- `POST /api/jira/{ticket_key}/trigger-pipeline`
- `GET /api/github`
- `GET /api/pipelines`
- `POST /api/pipelines/start`
- `GET /api/pull-requests`
- `GET /api/actions`
- `GET /api/reports`
- `GET /api/settings`
- `POST /api/assistant/ask`

## Run backend

```bash
uvicorn backend.main:app --reload
```

Backend runs on `http://127.0.0.1:8000` by default.

## Run frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://127.0.0.1:5173` by default.

You can override the API target with:

```bash
VITE_API_BASE=http://127.0.0.1:8000
```

## Tests

```bash
pytest -q backend/test_user_registration.py
```

## Notes

This implementation is a polished working prototype with realistic seeded data and complete page coverage for the requested modules. It is designed so you can later replace the mock responses in `backend/main.py` with live Jira, GitHub, Actions, vector DB, and LLM integrations.
