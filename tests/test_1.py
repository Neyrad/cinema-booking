from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_user():
    response = client.post(
        "/users/",
        params={"name": "Andrey", "email": "andrey@example.com"}
    )
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["name"] == "Andrey"
    assert json_data["email"] == "andrey@example.com"
    assert "id" in json_data
