from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from auth import get_current_user
import models
import database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

from auth import router as auth_router
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/users/")
def create_user(name: str, email: str, db: Session = Depends(database.get_db)):
    user = models.User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.post("/movies/")
def create_movie(title: str, description: str, db: Session = Depends(database.get_db)):
    movie = models.Movie(title=title, description=description)
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie

@app.post("/bookings/")
def book_movie(user_id: int, movie_id: int, db: Session = Depends(database.get_db)):
    booking = models.Booking(user_id=user_id, movie_id=movie_id)
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

@app.get("/bookings/")
def get_bookings(db: Session = Depends(database.get_db)):
    return db.query(models.Booking).all()

@app.get("/bookings/me")
def read_my_bookings(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Booking).filter(models.Booking.user_id == current_user.id).all()

