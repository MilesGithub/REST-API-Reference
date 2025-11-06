Pharma REST API
----------------
A sample REST API for a fictional pharmaceutical company. Built with FastAPI and SQLModel (SQLite).

Quick start:
1. python -m venv .venv && source .venv/bin/activate
2. pip install -r requirements.txt
3. uvicorn app.main:app --reload
4. Open http://127.0.0.1:8000/docs for interactive API docs

Example endpoints:
- POST /auth/token  -> obtain JWT for demo user
- GET /drugs       -> list drugs
- POST /drugs      -> create drug (auth required)
- GET /trials       -> list clinical trials
- POST /orders      -> create an order

