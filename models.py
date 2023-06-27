from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from typing import Optional


class Usuarios(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    apellido = Column(String)
    usuario = Column(String, unique=True, nullable=False)
    correo = Column(String)
    password = Column(String, nullable=False)
    role = Column(String)
    activo = Column(Boolean, default=False)


class Inventario(Base):
    __tablename__: str = 'inventario'

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String)
    presentacion = Column(String)
    lote = Column(String, nullable=False)
    estiba_n = Column(String)
    cantidad = Column(Integer)
    cuarto = Column(String)
    lado = Column(String)
    rack = Column(String)
    nivel = Column(String)
    posicion = Column(String)
    existente = Column(Boolean, default=True)
    estado = Column(String(9))
    detalles = Column(String(150))
    usuario_id = Column(ForeignKey('usuarios.id'))
