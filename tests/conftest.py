import os

# config for tests comes from the environment (12-factor III)
# This must happen before any import from app.

os.environ["SECRET_KEY"] = "test-secret-key-that-is-at-least-32-bytes"
os.environ["DATABSE_URL"] = "sqlite://"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import get_db, Base
from app.main import app


@pytest.fixture()
def client():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    TestingSession = sessionmaker(bind=engine, autoflush=False)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSession()
        try:
            yield db

        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def make_headers(client):
    """Register and log in user, and return their Authorization header."""

    def _make(username: str, password: str = "password123"):
        client.post("/auth/register", json={"username": username, "password": password})
        response = client.post(
            "/auth/login", data={"username": username, "password": password}
        )

        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    return _make
