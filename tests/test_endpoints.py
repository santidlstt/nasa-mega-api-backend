import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "endpoints" in data

def test_apod():
    response = client.get("/apod")
    assert response.status_code == 200
    data = response.json()
    # Verifica que haya campos esperados
    assert "date" in data or "url" in data

def test_neo():
    response = client.get("/neo?start_date=2025-09-01&end_date=2025-09-07&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 2

def test_mars_rover():
    response = client.get("/mars-rover?rover=curiosity&sol=1000&limit=3")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 3

def test_space_weather():
    response = client.get("/space-weather?date=2025-09-01")
    assert response.status_code == 200
    data = response.json()
    # Puede devolver message si no hay imágenes
    assert "message" in data or isinstance(data, list)
