from sqlalchemy import Column, Integer, String, CheckConstraint, Enum
from database import Base
import enum
from sqlalchemy import Column, Integer, String, Enum as SQLAlchemyEnum


class CareerEnum(enum.Enum):
    desarrollo_software = "Desarrollo de Software"
    ciencia_datos = "Ciencia de Datos"
    redes = "Redes"
    multimedia = "Multimedia"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    year_of_birth = Column(Integer)
    career = Column(SQLAlchemyEnum(CareerEnum))


