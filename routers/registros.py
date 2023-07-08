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


# Creación de una instancia del enrutador
router = APIRouter(prefix="/registros", tags=['registros'])

# Directorio de plantillaspara Jinja2
templates = Jinja2Templates(directory='templates')

# Sesión para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Consultar todos los registros
@router.get("/", response_class=HTMLResponse)
async def consultar_registros(request: Request, db: Session = Depends(get_db)):
    registros = db.query(Inventario).order_by(Inventario.id.desc()).all()
    return templates.TemplateResponse("home.html", {'request': request, 'registros': registros})


# Buscar por lote
@router.get("/buscar-lote/{lote}", response_class=HTMLResponse)
async def buscar_lote(request: Request, lote: str, db: Session = Depends(get_db)):
    batch_response = db.query(Inventario).filter(Inventario.lote == lote).first()
    return templates.TemplateResponse("buscar-lote.html", {'request': request, 'batch_data': batch_response})


# Crear registro nuevo
@router.get("/crear-registro", response_class=HTMLResponse)
async def crear_registro(request: Request):
    return templates.TemplateResponse("crear-registro.html", {'request': request})


@router.post("/crear-registro", response_class=HTMLResponse)
async def nuevo_registro(request: Request, tipo: str = Form(...), presentacion: str = Form(...), lote: str = Form(...),
                         estiba_n: str = Form(...), cantidad: int = Form(...), cuarto: str = Form(...),
                         lado: str = Form(...), rack: str = Form(...), nivel: str = Form(...), posicion: str = Form(...),
                         detalles: str = Form(...), db: Session = Depends(get_db)):

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

    RedirectResponse("/registros")

# Endpoint para edición de registros
@router.get("/editar-registro/{registro_id}", response_class=HTMLResponse)
async def editar_registro(request: Request, registro_id: int, db: Session = Depends(get_db)):
    reg = db.query(Inventario).filter(Inventario.id == registro_id).first()
    return templates.TemplateResponse("editar-registro.html", {'request': request, 'reg': reg})


# Editar registro
@router.post("/editar-registro/{registro_id}", response_class=HTMLResponse)
async def editar_registro(request: Request, registro_id: int, tipo: str = Form(...), presentacion: str = Form(...),
                          lote: str = Form(...), estiba_n: str = Form(...), cantidad: int = Form(...),
                          cuarto: str = Form(...), lado: str = Form(...), rack: str = Form(...), nivel: str = Form(...),
                          posicion: str = Form(...),detalles: Optional[str] = Form(None),
                          db: Session = Depends(get_db)):

    registro_editado = db.query(Inventario).filter(Inventario.id == registro_id).first()

    registro_editado.tipo = tipo
    registro_editado.presentacion = presentacion
    registro_editado.lote = lote
    registro_editado.estiba_n = estiba_n
    registro_editado.cantidad = cantidad
    registro_editado.cuarto = cuarto
    registro_editado.lado = lado
    registro_editado.rack = rack
    registro_editado.nivel = nivel
    registro_editado.posicion = posicion
    registro_editado.existente = True
    registro_editado.detalles = detalles

    db.add(registro_editado)
    db.commit()

    return RedirectResponse(url="/registros", status_code=status.HTTP_302_FOUND)


@router.post("/complete/{registro_id", response_class=HTMLResponse)
async def complete(request: Request, registro_id: int, db: Session = Depends(get_db)):
    registro = db.query(Inventario).filter(Inventario.id == registro_id).first()
    registro.existente = False
    db.add(registro)
    db.commit()


# ELiminar registro
@router.delete("/eliminar-registro/{registro_id}", response_class=HTMLResponse)
async def eliminar_registro(request: Request, registro_id: int, db: Session = Depends(get_db)):
    registro_eliminar = db.query(Inventario).filter(Inventario.id == registro_id).first()
    if not registro_eliminar:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro no encontrado")

    db.delete(registro_eliminar)
    db.commit()

    return RedirectResponse("/registros", status_code=status.HTTP_302_FOUND)








