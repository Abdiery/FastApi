from pydantic import BaseModel
from enum import Enum

# Definir el Enum en Pydantic también
class CareerEnum(str, Enum):
    desarrollo_software = "Desarrollo de Software"
    ciencia_datos = "Ciencia de Datos"
    redes = "Redes"
    multimedia = "Multimedia"

class UserCreate(BaseModel):
    name: str
    email: str
    year_of_birth: int
    career: CareerEnum  # Usar el Enum en el esquema

class User(BaseModel):
    id: int
    name: str
    email: str
    year_of_birth: int
    career: CareerEnum  # Usar el Enum en el esquema

    class Config:
     from_attributes = True

