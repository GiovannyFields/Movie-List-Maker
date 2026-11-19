import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from backend.database import get_session
from backend.main import app

# pytest automatically finds fixtures in conftest.py, so every test file can use them


@pytest.fixture
def client():
    # a brand new database that only lives in memory, so tests never touch movies.db.
    # StaticPool keeps it as one connection, otherwise each connection would get
    # its own empty in-memory db
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    # swap the real get_session for one that uses the test database
    def get_test_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_test_session
    yield TestClient(app)
    app.dependency_overrides.clear()


# a list that's already made, for tests that need one to exist first
@pytest.fixture
def horror_list(client):
    response = client.post(
        "/lists", json={"name": "Friday Horror Night", "description": "scary stuff"}
    )
    return response.json()
