from fastapi.testclient import TestClient
from app.main import app
from app.models import User, Movie, Booking
from app.database import SessionLocal, engine
from sqlalchemy.orm import Session
import pytest

client = TestClient(app)

@pytest.fixture(scope="module")
def db():
    db = SessionLocal()
    yield db
    db.close()

def test_create_movie(db):
    response = client.post(
        "/movies/",
        params={"title": "Test Movie 0", "description": "Test Description 0"}
    )
    assert response.status_code == 200

def test_book_movie(db):
    user = User(name="Test User", email="test@example.com")
    db.add(user)
    db.commit()
    db.refresh(user)

    movie = Movie(title="Test Movie", description="Test Description")
    db.add(movie)
    db.commit()
    db.refresh(movie)

    response = client.post(
        "/bookings/",
        params={"user_id": user.id, "movie_id": movie.id}
    )
    assert response.status_code == 200


def test_get_bookings(db):
    response = client.get("/bookings/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

from app.auth import create_access_token

def test_read_my_bookings(db):
    user = User(name="Test User228", email="testuser228@example.com", password_hash="hashed")
    db.add(user)
    db.commit()
    db.refresh(user)

    movie = Movie(title="Test Movie228", description="Just testing")
    db.add(movie)
    db.commit()
    db.refresh(movie)

    booking = Booking(user_id=user.id, movie_id=movie.id)
    db.add(booking)
    db.commit()

    token = create_access_token({"sub": user.email})

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/bookings/me", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["user_id"] == user.id
