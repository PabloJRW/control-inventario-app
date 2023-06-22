from fastapi import FastAPI, Depends, HTTPException, Path
from database import SessionLocal, engine
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
import models
from models import Inventario
from pydantic import BaseModel, Field
import opciones_validas


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
async def read_all(db: db_dependency):
    return db.query(Inventario).all()



class InventarioRequest(BaseModel):
    tipo:str = opciones_validas.TipoOpciones
    presentacion:str = opciones_validas.PresentacionOpciones
    lote:str = Field(min_length=8, max_lenght=8)
    estiba_n:str = Field()
    cantidad:int = Field(gt=0)
    cuarto:str = opciones_validas.CuartoOpciones
    lado:str = opciones_validas.LadoOpciones
    rack:str = opciones_validas.RackOpciones
    nivel:str = opciones_validas.NivelOpciones
    posicion:str = opciones_validas.PosicionOpciones
    existente:bool

# Crear registro nuevo
@app.post("/registros/nuevo_registro", status_code=status.HTTP_201_CREATED)
async def crear_registro(db:db_dependency, inv_request:InventarioRequest):
    inv_model = Inventario(**inv_request.dict())
    db.add(inv_model)
    db.commit()




@app.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db:db_dependency, inv_request:InventarioRequest, inv_id: int=Path(gt=0)):
    inv_model = db.query(Inventario).filter(Inventario.id==inv_id).first()
    if inv_model is None:
        raise HTTPException(status_code=404, detail="Todo not found!.")
    
    inv_model.tipo = inv_request.tipo
    inv_model.presentacion = inv_request.presentacion
    inv_model.lote = inv_request.lote
    inv_model.estiba_n = inv_request.estiba_n
    inv_model.estiba_n = inv_request.estiba_n
    inv_model.estiba_n = inv_request.estiba_n
    inv_model.estiba_n = inv_request.estiba_n
    inv_model.estiba_n = inv_request.estiba_n
    db.add(inv_model)
    db.commit()