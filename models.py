from database import Base
from sqlalchemy import Column, Integer, String, Boolean


class Inventario(Base):
    __tablename__='inventario'

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String)
    presentacion = Column(String)
    lote = Column(String)
    estiba_n = Column(String)
    cantidad = Column(Integer)
    cuarto = Column(String)
    lado = Column(String)
    rack = Column(String)
    nivel = Column(String)
    posicion = Column(String)
    existente = Column(Boolean, default=True)
