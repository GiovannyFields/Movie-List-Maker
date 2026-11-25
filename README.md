# Movie List Maker

Make movie lists and add movies to them. The Discover page shows one movie at a time, left arrow skips it and right arrow adds it.

- Backend: FastAPI + SQLModel (SQLite)
- Frontend: Flask
- Tests: pytest

## Setup

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run

Start the API first, then the frontend in a second terminal.

```
uvicorn backend.main:app --reload
flask --app frontend.app run
```

- Website: http://localhost:5000
- API docs: http://localhost:8000/docs

## Tests

```
pytest
```
