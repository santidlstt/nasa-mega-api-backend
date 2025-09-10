from fastapi.testclient import TestClient
from datetime import date, timedelta
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "endpoints" in data

def test_apod():
    today = date.today().isoformat()
    response = client.get(f"/apod?date={today}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)

def test_apod_invalid_date():
    response = client.get("/apod?date=2025-13-01") 
    assert response.status_code == 422  

def test_neo():
    start = (date.today() - timedelta(days=3)).isoformat()
    end = date.today().isoformat()
    response = client.get(f"/neo?start_date={start}&end_date={end}&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 5

def test_neo_exceed_range():
    start = (date.today() - timedelta(days=10)).isoformat()
    end = date.today().isoformat()
    response = client.get(f"/neo?start_date={start}&end_date={end}")
    assert response.status_code == 400  

def test_mars_rover():
    response = client.get("/mars-rover?rover=curiosity&sol=1000&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 5

def test_mars_rover_invalid_sol():
    response = client.get("/mars-rover?rover=curiosity&sol=-1")
    assert response.status_code == 422  

def test_space_weather():
    today = date.today().isoformat()
    response = client.get(f"/space-weather?date={today}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list) or "message" in data

def test_space_weather_before_min_date():
    response = client.get("/space-weather?date=2015-06-01")
    assert response.status_code == 400  

def test_space_weather_invalid_date():
    response = client.get("/space-weather?date=2025-13-01")  
    assert response.status_code == 422