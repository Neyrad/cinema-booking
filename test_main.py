from fastapi.testclient import TestClient
from main import app  # Імпортуємо FastAPI додаток з main.py

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200  # Перевіряємо, чи статус 200 OK
    assert response.json() == {"message": "Hello World"}  # Перевіряємо, чи повертається правильне повідомлення

