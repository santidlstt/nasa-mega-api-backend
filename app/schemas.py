from pydantic import BaseModel, Field, field_validator
from datetime import date as DateType
from typing import Optional

class ApodRequest(BaseModel):
    date: Optional[DateType] = Field(
        None, description="Fecha opcional (YYYY-MM-DD)"
    )

class NeoRequest(BaseModel):
    start_date: DateType = Field(..., description="Fecha de inicio (YYYY-MM-DD)")
    end_date: DateType = Field(..., description="Fecha de fin (YYYY-MM-DD)")
    limit: int = Field(
        10,
        ge=1,
        le=100,
        description="Máximo de resultados (1-100)"
    )

    @field_validator("end_date")
    def validate_end_date(cls, v, info):
        start_date = info.data.get("start_date")
        if start_date and v < start_date:
            raise ValueError("La fecha de fin no puede ser anterior a la fecha de inicio.")
        delta = (v - start_date).days
        if delta > 7:
            raise ValueError("El rango máximo permitido es de 7 días.")
        return v

class MarsRoverRequest(BaseModel):
    rover: Optional[str] = Field(
        "curiosity",
        description="Nombre del rover (curiosity, opportunity, spirit)"
    )
    sol: Optional[int] = Field(
        None,
        ge=0,
        description="Día marciano desde inicio de misión"
    )
    camera: Optional[str] = Field(
        None, description="Cámara opcional (FHAZ, RHAZ, NAVCAM, etc.)"
    )
    limit: int = Field(
        20,
        ge=1,
        le=100,
        description="Máximo de fotos (1-100)"
    )

class SpaceWeatherRequest(BaseModel):
    date: DateType = Field(..., description="Fecha requerida (YYYY-MM-DD, mínima: 2015-06-13)")

    @field_validator("date")
    def validate_date(cls, v):
        min_date = DateType(2015, 6, 13)
        if v < min_date:
            raise ValueError(f"No hay imágenes disponibles antes de {min_date.isoformat()}.")
        return v
