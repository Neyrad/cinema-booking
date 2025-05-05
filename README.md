# Cinema Booking API

This is a simple API for booking movie tickets, made with **FastAPI**, **SQLAlchemy**, and **SQLite**.

## Features

* User registration and login (JWT tokens)
* Add and view movies
* Book tickets for movies
* View your own bookings (auth required)

## Tech Stack

* Python 3
* FastAPI
* SQLAlchemy
* SQLite
* Pytest

## Installation

```bash
git clone https://github.com/Neyrad/cinema-booking.git
cd cinema-booking
python -m venv env
source env/bin/activate  # or use the appropriate command on Windows
pip install -r requirements.txt
```

## Run the App

```bash
uvicorn app.main:app --reload
```

Open in browser: `http://127.0.0.1:8000/docs`

## Authentication

* Register: `POST /auth/register`
* Login: `POST /auth/token`
* Use the token with the `Authorization: Bearer <token>` header

## Running Tests

```bash
./test.sh
```

## Project Structure

```
app/
  auth.py
  database.py
  main.py
  models.py
tests/
  test_1.py
  test_2.py
requirements.txt
test.sh
test.db
```

---
