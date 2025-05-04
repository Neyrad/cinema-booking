from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
import database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/")
def create_user(name: str, email: str, db: Session = Depends(get_db)):
    user = models.User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.post("/movies/")
def create_movie(title: str, description: str, db: Session = Depends(get_db)):
    movie = models.Movie(title=title, description=description)
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie

@app.post("/bookings/")
def book_movie(user_id: int, movie_id: int, db: Session = Depends(get_db)):
    booking = models.Booking(user_id=user_id, movie_id=movie_id)
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

@app.get("/bookings/")
def get_bookings(db: Session = Depends(get_db)):
    return db.query(models.Booking).all()
