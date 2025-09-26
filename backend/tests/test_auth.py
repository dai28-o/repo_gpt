from typing import Generator
import os

os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('DATABASE_URL', 'sqlite:///./test.db')

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.database import Base, get_db
from app.main import app


@pytest.fixture()
def db_session(tmp_path) -> Generator[Session, None, None]:
    test_db_url = f"sqlite:///{tmp_path / 'test.db'}"
    engine = create_engine(test_db_url)
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield session
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


@pytest.fixture()
def client(db_session):
    return TestClient(app)


def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "user@example.com",
            "password": "password123",
            "full_name": "Test User",
            "role": "participant",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "user@example.com"


def test_login_user(client):
    client.post(
        "/auth/register",
        json={
            "email": "login@example.com",
            "password": "password123",
            "full_name": "Login User",
            "role": "participant",
        },
    )
    response = client.post(
        "/auth/token",
        data={"username": "login@example.com", "password": "password123"},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
