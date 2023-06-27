from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from typing import Annotated, Optional
from database import SessionLocal
from models import Usuarios
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()
bcrypt_ctx = CryptContext(schemes=['bcrypt'], deprecated='auto')


class CreateUserRequest(BaseModel):
    nombre: str
    apellido: str
    usuario: str
    correo: Optional[str]
    password: str
    role: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def authenticated_user(usuario: str,  password: str, db):
    usuario = db.query(Usuarios).filter(Usuarios.usuario == usuario).first()
    if not usuario:
        return False
    if not bcrypt_ctx.verify(usuario.password == password):
        return False
    return "Succesful login."


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_new_user = Usuarios(
        nombre=create_user_request.nombre,
        apellido=create_user_request.apellido,
        usuario=create_user_request.usuario,
        password=bcrypt_ctx.hash(create_user_request.password),
        role=create_user_request.role
    )
    return create_new_user


@router.post("/token")
async def login_access_for_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return form_data

