from fastapi import FastAPI
import models
from config import engine
import api.routers

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api.routers.router)
