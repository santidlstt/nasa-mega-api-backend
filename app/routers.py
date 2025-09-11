from fastapi import APIRouter, Depends
from app import services
from app.schemas import ApodRequest, NeoRequest, MarsRoverRequest, SpaceWeatherRequest

router = APIRouter()

@router.get("/")
async def root():
    return {
        "message": "🚀 Bienvenido al NASA Mega API Backend!",
        "docs": "/docs",
        "endpoints": [
            { "url": "/apod", "description": "Astronomy Picture of the Day" },
            { "url": "/neo", "description": "Near Earth Objects" },
            { "url": "/mars-rover", "description": "Fotos de Marte" },
            { "url": "/space-weather", "description": "Imágenes EPIC de la Tierra" }
        ]
    }

@router.get("/apod")
async def get_apod(params: ApodRequest = Depends()):
    return await services.fetch_apod(date=params.date)

@router.get("/neo")
async def get_neo(params: NeoRequest = Depends()):
    # Ya no validamos rango ni fechas, lo hace NeoRequest con @field_validator
    return await services.fetch_neo(
        start_date=params.start_date,
        end_date=params.end_date,
        limit=params.limit
    )

@router.get("/mars-rover")
async def get_mars_rover(params: MarsRoverRequest = Depends()):
    return await services.fetch_mars_rover(
        rover=params.rover,
        sol=params.sol,
        camera=params.camera,
        limit=params.limit
    )

@router.get("/space-weather")
async def get_space_weather(params: SpaceWeatherRequest = Depends()):
    # Validación de fecha mínima eliminada, la hace Pydantic
    return await services.fetch_space_weather(date=params.date)
