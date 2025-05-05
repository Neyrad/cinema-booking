"""Main application module for the FastAPI cinema booking project."""

from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.auth import get_current_user, router as auth_router
import app.models as models
import app.database as database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(auth_router)

from fastapi import HTTPException

# ---------------- USERS ----------------

@app.get("/users/")
def get_users(db: Session = Depends(database.get_db)):
    return db.query(models.User).all()

@app.put("/users/{user_id}")
def update_user(user_id: int, name: str, email: str, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = name
    user.email = email
    db.commit()
    db.refresh(user)
    return user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}

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


# ---------------- MOVIES ----------------

@app.get("/movies/")
def get_movies(db: Session = Depends(database.get_db)):
    return db.query(models.Movie).all()

@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, title: str, description: str, db: Session = Depends(database.get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    movie.title = title
    movie.description = description
    db.commit()
    db.refresh(movie)
    return movie

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(database.get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    db.delete(movie)
    db.commit()
    return {"message": "Movie deleted"}

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

@app.get("/movies/recommend")
def recommend_movies(top_n: int = Query(5, ge=1), db: Session = Depends(database.get_db)):
    """
    Recommend the top N most popular movies based on number of bookings.
    """
    results = (
        db.query(models.Movie.title, models.Movie.description, func.count(models.Booking.id).label("bookings"))
        .join(models.Booking, models.Movie.id == models.Booking.movie_id)
        .group_by(models.Movie.id)
        .order_by(func.count(models.Booking.id).desc())
        .limit(top_n)
        .all()
    )

    return [{"title": r.title, "description": r.description, "bookings": r.bookings} for r in results]

# ---------------- BOOKINGS ----------------

@app.get("/bookings/{booking_id}")
def get_booking(booking_id: int, db: Session = Depends(database.get_db)):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@app.put("/bookings/{booking_id}")
def update_booking(booking_id: int, user_id: int, movie_id: int, db: Session = Depends(database.get_db)):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    booking.user_id = user_id
    booking.movie_id = movie_id
    db.commit()
    db.refresh(booking)
    return booking

@app.delete("/bookings/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(database.get_db)):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(booking)
    db.commit()
    return {"message": "Booking deleted"}

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

# ----------------------------------------------------

@app.get("/mybookings/")
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

