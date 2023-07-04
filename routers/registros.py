from fastapi import APIRouter, Depends, HTTPException, Path, Request, Form
from database import SessionLocal
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import RedirectResponse
from models import Inventario
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(prefix="/registros", tags=['registros'])

templates = Jinja2Templates(directory='templates')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


# Consultar todos los registros
@router.get("/", response_class=HTMLResponse)
async def consultar_registros(request: Request, db: Session = Depends(get_db)):
    registros = db.query(Inventario).order_by(Inventario.id.desc()).all()
    return templates.TemplateResponse("home.html", {'request': request, 'registros': registros})


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
@router.get("/crear-registro", response_class=HTMLResponse)
async def crear_registro(request: Request):
    return templates.TemplateResponse("crear-registro.html", {'request': request})


@router.post("/crear-registro", response_class=HTMLResponse)
async def nuevo_registro(request: Request, tipo: str = Form(...), presentacion: str = Form(...),
                          lote: str = Form(...), estiba_n: str = Form(...), cantidad: int = Form(...),
                          cuarto: str = Form(...), lado: str = Form(...), rack: str = Form(...),
                          nivel: str = Form(...), posicion: str = Form(...),
                          detalles: str = Form(...),
                          db: Session = Depends(get_db)):

    nuevo_registro = Inventario()
    nuevo_registro.tipo = tipo
    nuevo_registro.presentacion = presentacion
    nuevo_registro.lote = lote
    nuevo_registro.estiba_n = estiba_n
    nuevo_registro.cantidad = cantidad
    nuevo_registro.cuarto = cuarto
    nuevo_registro.lado = lado
    nuevo_registro.rack = rack
    nuevo_registro.nivel = nivel
    nuevo_registro.posicion = posicion
    nuevo_registro.existente = True
    nuevo_registro.detalles = detalles

    db.add(nuevo_registro)
    db.commit()

    return RedirectResponse(url="/registros", status_code=status.HTTP_302_FOUND)


@router.get("/editar-registro", response_class=HTMLResponse)
async def editar_registro(request: Request):
    return templates.TemplateResponse("editar-registro.html", {'request': request})


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


