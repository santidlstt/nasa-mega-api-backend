import httpx
from datetime import datetime, timedelta, date as DateType
from .config import NASA_API_KEY

BASE_URL = "https://api.nasa.gov"

async def fetch_apod(date: DateType = None):
    url = f"{BASE_URL}/planetary/apod"
    params = {"api_key": NASA_API_KEY}
    if date:
        params["date"] = date.isoformat()
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
    if resp.status_code != 200:
        return {"error": f"Error en la API de NASA: {resp.status_code}"}
    data = resp.json()
    return {
        "title": data.get("title"),
        "date": data.get("date"),
        "explanation": data.get("explanation"),
        "url": data.get("url"),
        "media_type": data.get("media_type")
    }

async def fetch_neo(start_date: DateType, end_date: DateType, limit: int = 10):
    delta = timedelta(days=7)
    results = []

    current_start = start_date
    while current_start <= end_date:
        current_end = min(current_start + delta - timedelta(days=1), end_date)
        url = f"{BASE_URL}/neo/rest/v1/feed"
        params = {
            "start_date": current_start.isoformat(),
            "end_date": current_end.isoformat(),
            "api_key": NASA_API_KEY
        }
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params)
        if resp.status_code != 200:
            return {"error": f"Error en la API de NASA: {resp.status_code}"}
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

    return results[:limit]

async def fetch_mars_rover(rover: str = "curiosity", sol: int = 1000, camera: str = None, limit: int = 20):
    url = f"{BASE_URL}/mars-photos/api/v1/rovers/{rover}/photos"
    params = {"sol": sol, "api_key": NASA_API_KEY}
    if camera:
        params["camera"] = camera
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
    if resp.status_code != 200:
        return {"error": f"Error en la API de NASA: {resp.status_code}"}
    data = resp.json()
    photos = [
        {"id": p["id"], "img_src": p["img_src"], "earth_date": p["earth_date"], "camera": p["camera"]["full_name"]}
        for p in data.get("photos", [])
    ]
    return photos[:limit]

async def fetch_space_weather(date: DateType):
    if date < DateType(2015, 6, 13):
        return {"error": "La fecha mínima es 2015-06-13."}

    url = f"{BASE_URL}/EPIC/api/natural/date/{date.isoformat()}"
    params = {"api_key": NASA_API_KEY}
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
    if resp.status_code != 200 or not resp.json():
        return {"message": f"No se encontraron imágenes para la fecha {date.isoformat()}."}
    data = resp.json()
    return [
        {
            "image": f"https://epic.gsfc.nasa.gov/archive/natural/{date.strftime('%Y/%m/%d')}/png/{item['image']}.png",
            "caption": item["caption"],
            "date": item["date"]
        }
        for item in data
    ]
