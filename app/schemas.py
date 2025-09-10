from pydantic import BaseModel, Field
from datetime import date as DateType
from typing import Optional

class ApodRequest(BaseModel):
    date: Optional[DateType] = Field(None, description="Fecha opcional (YYYY-MM-DD)") 

class NeoRequest(BaseModel):
    start_date: DateType = Field(..., description="Fecha de inicio (YYYY-MM-DD)")
    end_date: DateType = Field(..., description="Fecha de fin (YYYY-MM-DD)")
    limit: int = Field(10, ge = 1, le = 100, description= "Máximo de resultados (1-100)")

class MarsRoverRequest(BaseModel):
    rover: Optional[str] = Field("curiosity", description="Nombre del rover (curiosity, opportunity, spirit)")
    sol: Optional[int] = Field(None, ge=0, description="Día marciano desde inicio de misión")
    camera: Optional[str] = Field(None, description="Cámara opcional (FHAZ, RHAZ, NAVCAM, etc.)")
    limit: int = Field(20, ge=1, le=100, description="Máximo de fotos (1-100)")

class SpaceWeatherRequest(BaseModel):
    date: DateType = Field(..., description="Fecha requerida (YYYY-MM-DD, mínima: 2015-06-13)") 