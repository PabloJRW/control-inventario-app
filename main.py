from fastapi import FastAPI
from database import engine
import models
from routers import registros, auth

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(registros.router)
app.include_router(auth.router)
