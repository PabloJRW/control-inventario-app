from fastapi import APIRouter, Depends, HTTPException, Path, Request
from database import SessionLocal
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from starlette import status
from models import Inventario
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(prefix="/registro", tags=['registro'])

templates = Jinja2Templates(directory='templates')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/home")
async def home(request:Request):
    return templates.TemplateResponse("home.html", {'request': request})


@router.get("/test")
async def test(request:Request):
    return templates.TemplateResponse("nuevo_registro.html", {'request': request})


# Consultar todos los registros
@router.get("/", status_code=status.HTTP_200_OK)
async def consultar_registros(db: db_dependency):
    return db.query(Inventario).order_by(Inventario.id.desc()).all()


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
    detalles: Optional[str] = Field()


# Crear registro nuevo
@router.post("/registros/nuevo_registro", status_code=status.HTTP_201_CREATED)
async def crear_registro(db: db_dependency, inv_request: InventarioRequest):
    inv_model = Inventario(**inv_request.dict())
    db.add(inv_model)
    db.commit()


@router.put("/registros/{inv_id}", status_code=status.HTTP_204_NO_CONTENT)
async def actualizar_registro(db: db_dependency, inv_request: InventarioRequest, inv_id: int = Path(gt=0)):
    inv_model = db.query(Inventario).filter(Inventario.id == inv_id).first()
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


@router.get("/registros/{lote}", status_code=status.HTTP_200_OK)
async def buscar_lote(db: db_dependency, lote: int = Path(gt=0)):
    inv_model = db.query(Inventario).filter(Inventario.lote == lote).all()
    if inv_model is not None:
        return inv_model
    raise HTTPException(status_code=404)


@router.delete("/delete/{id_registro}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_registro(db: db_dependency, id_registro: int = Path(gt=0)):
    model = db.query(Inventario).filter(Inventario.id == id_registro).first()
    if model is None:
        raise HTTPException(status_code=404, detail="Todo not found!.")

    db.query(Inventario).filter(Inventario.id == id_registro).delete()
    db.commit()


