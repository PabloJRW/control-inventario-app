from fastapi import FastAPI, Depends, HTTPException, Path
from database import SessionLocal, engine
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
import models
from models import Inventario
from pydantic import BaseModel, Field
from opciones_validas import TipoOpciones, PresentacionOpciones, CuartoOpciones
from opciones_validas import LadoOpciones, RackOpciones, NivelOpciones, PosicionOpciones

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


# Consultar todos los registros
@app.get("/", status_code=status.HTTP_200_OK)
async def consultar_registros(db: db_dependency):
    return db.query(Inventario).all()


class InventarioRequest(BaseModel):
    tipo: str = Field()
    presentacion: str = Field()
    lote: str = Field(min_length=8, max_lenght=8)
    estiba_n: str = Field()
    cantidad: int = Field(gt=0)
    cuarto: str = Field()
    lado: str = Field()
    rack: str = Field()
    nivel: str = Field()
    posicion: str = Field()
    existente: bool
    estado: str = Field()
    detalles: str = Field()

# Crear registro nuevo
@app.post("/registros/nuevo_registro", status_code=status.HTTP_201_CREATED)
async def crear_registro(db:db_dependency, inv_request:InventarioRequest):
    inv_model = Inventario(**inv_request.dict())
    db.add(inv_model)
    db.commit()




@app.put("/registros/{inv_id}", status_code=status.HTTP_204_NO_CONTENT)
async def actualizar_registro(db:db_dependency, inv_request:InventarioRequest, inv_id: int=Path(gt=0)):
    inv_model = db.query(Inventario).filter(Inventario.id==inv_id).first()
    if inv_model is None:
        raise HTTPException(status_code=404, detail="Todo not found!.")
    
    inv_model.tipo = inv_request.tipo
    inv_model.presentacion = inv_request.presentacion
    inv_model.lote = inv_request.lote
    inv_model.estiba_n = inv_request.estiba_n
    inv_model.cantidad = inv_request.cantidad
    inv_model.cuarto = inv_request.cuarto
    inv_model.lado = inv_request.lado
    inv_model.rack = inv_request.rack
    inv_model.nivel = inv_request.nivel
    inv_model.posicion = inv_request.posicion
    inv_model.existente = inv_request.existente
    db.add(inv_model)
    db.commit()



@app.get("/registros/{lote}", status_code=status.HTTP_200_OK)
async def buscar_lote(db: db_dependency, lote: int =Path(gt=0)):
    inv_model = db.query(Inventario).filter(Inventario.lote==lote).all()
    if inv_model is not None:
        return inv_model
    raise HTTPException(status_code=404, datail="ToDo not found.")