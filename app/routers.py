from fastapi import APIRouter, Query
from .services import get_apod, get_neo, get_mars_rover_photos, get_epic_images

router = APIRouter()

@router.get("/", summary="Bienvenida al API", description="Guía rápida para usar la NASA Mega API Backend")
def root():
    return {
        "message": "🚀 Bienvenido al NASA Mega API Backend!",
        "docs": "Visita /docs para acceder a la documentación Swagger UI y probar los endpoints.",
        "endpoints": [
            {
                "url": "/apod",
                "description": "Astronomy Picture of the Day: imagen del día, título y explicación."
            },
            {
                "url": "/neo",
                "description": "Near Earth Objects: asteroides cercanos entre fechas. Máximo 7 días por request, pero el backend combina rangos automáticamente. Se puede usar 'limit' para acotar resultados."
            },
            {
                "url": "/mars-rover",
                "description": "Fotos de Marte por rover y sol marciano. Se puede filtrar por cámara y limitar la cantidad de fotos con 'limit'. Ejemplos de rover: curiosity, opportunity, spirit."
            },
            {
                "url": "/space-weather",
                "description": "Imágenes EPIC de la Tierra desde el espacio por fecha. Fecha mínima: 2015-06-13. No todas las fechas tienen imágenes."
            }
        ],
        "notes": "Todos los endpoints devuelven JSON listo para consumir y se pueden probar en Swagger UI (/docs)."
    }


@router.get(
        "/apod",
        summary="Astronomy Picture of the Day",
        description=("Devuelve la imagen del día, el título y la explicación.\n"
        "Opcional: 'date' para devolver la imagen de una fecha concreta.\n"
        "Si no se proporciona 'date', se devuelve la imagen del dia actual."))
def apod(date: str = Query(None, description="YYYY-MM-DD")):
    return get_apod(date)

@router.get(
        "/neo",
        summary="Near Earth Objects",
        description=("Devuelve asteroides cercanos a la Tierra entre fechas.\n"
        "El backend maneja automáticamente rangos de hasta 7 días por request.\n"
        "Opcional: 'limit' para acotar la cantidad de resultados devueltos.\n"))
def neo(
    start_date: str = Query(..., description="Fecha inicio YYYY-MM-DD"),
    end_date: str = Query(..., description="Fecha fin YYYY-MM-DD"),
    limit: int = Query(None, description="Cantidad máxima de asteroides a devolver")
):
    return get_neo(start_date, end_date, limit)

@router.get(
        "/mars-rover",
        summary="Mars Rover Photos",
        description=("Devuelve fotos de Marte por rover y sol marciano.\n"))
def mars_rover(
    rover: str = Query("curiosity", description="Nombre del rover. Ejemplos: curiosity, opportunity, spirit"),
    sol: int = Query(1000, description="Día marciano desde el inicio de la misión del rover"),
    camera: str = Query(None, description="Cámara opcional: FHAZ, RHAZ, NAVCAM, etc."),
    limit: int = Query(20, description="Cantidad máxima de fotos a devolver")
):
    return get_mars_rover_photos(rover, sol, camera, limit)

@router.get(
        "/space-weather",
        summary="EPIC Earth Images",
        description=("Devuelve imágenes EPIC de la Tierra desde el espacio por fecha.\n"
                    "Puede que no todas las fechas tengan imágenes.\n"))
def space_weather(
    date: str = Query(..., description="YYYY-MM-DD. Fecha mínima: 2015-06-13")
):
    return get_epic_images(date)
