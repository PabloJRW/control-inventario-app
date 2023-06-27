from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from typing import Annotated, Optional
from database import SessionLocal
from models import Usuarios
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

router = APIRouter(prefix="/auth", tags=['auth'])

SECRET_KEY = "2b5a7a6b202bf5e9b5d7e9a6e635350583eaeec2f0703e38418fc07ad3ccc5ff"
ALGORITHM = "HS256"

bcrypt_ctx = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


class CreateUserRequest(BaseModel):
    nombre: str
    apellido: str
    usuario: str
    correo: Optional[str]
    password: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def authenticated_user(usuario: str,  password: str, db):
    user = db.query(Usuarios).filter(Usuarios.usuario == usuario).first()
    if not user:
        return False
    if not bcrypt_ctx.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')

        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_new_user = Usuarios(
        nombre=create_user_request.nombre,
        apellido=create_user_request.apellido,
        usuario=create_user_request.usuario,
        hashed_password=bcrypt_ctx.hash(create_user_request.password),
        role=create_user_request.role
    )
    db.add(create_new_user)
    db.commit()


@router.post("/token")
async def login_access_for_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticated_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    token = create_access_token(user.usuario, user.id, timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}

