"""Main application module for the FastAPI cinema booking project."""

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.auth import get_current_user, router as auth_router
import app.models as models
import app.database as database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(auth_router)

@app.get("/")
def read_root():
    """
    Root endpoint that returns a simple greeting.

    Returns:
        dict: Greeting message.
    """
    return {"message": "Hello World"}

@app.post("/users/")
def create_user(name: str, email: str, db: Session = Depends(database.get_db)):
    """
    Create a new user.

    Args:
        name (str): User's name.
        email (str): User's email.
        db (Session): SQLAlchemy session.

    Returns:
        User: The created user.
    """
    user = models.User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.post("/movies/")
def create_movie(title: str, description: str, db: Session = Depends(database.get_db)):
    """
    Create a new movie.

    Args:
        title (str): Movie title.
        description (str): Movie description.
        db (Session): SQLAlchemy session.

    Returns:
        Movie: The created movie.
    """
    movie = models.Movie(title=title, description=description)
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie

@app.post("/bookings/")
def book_movie(user_id: int, movie_id: int, db: Session = Depends(database.get_db)):
    """
    Book a movie for a user.

    Args:
        user_id (int): ID of the user.
        movie_id (int): ID of the movie.
        db (Session): SQLAlchemy session.

    Returns:
        Booking: The created booking.
    """
    booking = models.Booking(user_id=user_id, movie_id=movie_id)
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

@app.get("/bookings/")
def get_bookings(db: Session = Depends(database.get_db)):
    """
    Get all bookings in the system.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        list[Booking]: List of all bookings.
    """
    return db.query(models.Booking).all()

@app.get("/bookings/me")
def read_my_bookings(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Get bookings made by the current authenticated user.

    Args:
        db (Session): SQLAlchemy session.
        current_user (User): The currently authenticated user.

    Returns:
        list[Booking]: List of user's bookings.
    """
    return db.query(models.Booking).filter(models.Booking.user_id == current_user.id).all()
