import requests
from datetime import datetime, timedelta
from .config import NASA_API_KEY

BASE_URL = "https://api.nasa.gov"

def get_apod(date=None):
    url = f"{BASE_URL}/planetary/apod"
    params = {"api_key": NASA_API_KEY}
    if date:
        params["date"] = date
    response = requests.get(url, params=params)
    return response.json()

def get_neo(start_date, end_date, limit=None):
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        return {"error": "Formato de fecha inválido. Use YYYY-MM-DD."}

    delta = timedelta(days=7)
    results = []

    current_start = start
    while current_start <= end:
        current_end = min(current_start + delta - timedelta(days=1), end)
        url = f"{BASE_URL}/neo/rest/v1/feed"
        params = {
            "start_date": current_start.strftime("%Y-%m-%d"),
            "end_date": current_end.strftime("%Y-%m-%d"),
            "api_key": NASA_API_KEY
        }
        resp = requests.get(url, params=params)
        data = resp.json()
        for date_key in data.get("near_earth_objects", {}):
            for neo in data["near_earth_objects"][date_key]:
                results.append({
                    "name": neo["name"],
                    "diameter_min": neo["estimated_diameter"]["meters"]["estimated_diameter_min"],
                    "diameter_max": neo["estimated_diameter"]["meters"]["estimated_diameter_max"],
                    "is_potentially_hazardous": neo["is_potentially_hazardous_asteroid"],
                    "close_approach_date": neo["close_approach_data"][0]["close_approach_date"],
                    "relative_velocity_km_s": neo["close_approach_data"][0]["relative_velocity"]["kilometers_per_second"],
                    "miss_distance_km": neo["close_approach_data"][0]["miss_distance"]["kilometers"]
                })
        current_start = current_end + timedelta(days=1)

    if limit:
        results = results[:limit]
    return results

def get_mars_rover_photos(rover="curiosity", sol=1000, camera=None, limit=20):
    url = f"{BASE_URL}/mars-photos/api/v1/rovers/{rover}/photos"
    params = {"sol": sol, "api_key": NASA_API_KEY}
    if camera:
        params["camera"] = camera
    response = requests.get(url, params=params)
    data = response.json()
    photos = [{"id": p["id"], "img_src": p["img_src"], "earth_date": p["earth_date"], "camera": p["camera"]["full_name"]}
                for p in data.get("photos", [])]
    return photos[:limit]

def get_epic_images(date):
    try:
        dt = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return {"error": "Formato de fecha inválido. Use YYYY-MM-DD."}

    if dt < datetime(2015, 6, 13):
        return {"error": "La fecha mínima es 2015-06-13."}

    url = f"{BASE_URL}/EPIC/api/natural/date/{date}"
    params = {"api_key": NASA_API_KEY}
    response = requests.get(url, params=params)

    if response.status_code != 200 or not response.json():
        return {"message": f"No se encontraron imágenes para la fecha {date}."}

    data = response.json()
    return [{
        "image": f"https://epic.gsfc.nasa.gov/archive/natural/{date.replace('-', '/')}/png/{item['image']}.png",
        "caption": item["caption"],
        "date": item["date"]
    } for item in data]