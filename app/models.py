"""Database models for the cinema booking application."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    """
    Database model for a user.

    Attributes:
        id (int): Primary key.
        name (str): Name of the user.
        email (str): Email address (unique).
        password_hash (str): Hashed user password.
        bookings (list[Booking]): List of bookings made by the user.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)

    bookings = relationship("Booking", back_populates="user")


class Movie(Base):
    """
    Database model for a movie.

    Attributes:
        id (int): Primary key.
        title (str): Title of the movie.
        description (str): Description of the movie.
        bookings (list[Booking]): List of bookings for this movie.
    """
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)

    bookings = relationship("Booking", back_populates="movie")


class Booking(Base):
    """
    Database model for a movie booking.

    Attributes:
        id (int): Primary key.
        user_id (int): Foreign key to User.
        movie_id (int): Foreign key to Movie.
        timestamp (datetime): Booking time (defaults to now).
        user (User): Associated user.
        movie (Movie): Associated movie.
    """
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="bookings")
    movie = relationship("Movie", back_populates="bookings")
