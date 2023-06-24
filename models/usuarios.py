from config.database import Base
from sqlalchemy import Column, Integer, String, Boolean


class Usuarios(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String, unique=True, nullable=False)
    nombre = Column(String)
    apellido = Column(String)
    correo = Column(String)
    password = Column(String, nullable=False)
    role = Column(String)
    activo = Column(Boolean, default=False)



