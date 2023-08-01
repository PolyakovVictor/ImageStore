from fastapi import FastAPI
import models
from config import engine
import route

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/')
async def Home():
    return "Welcome Home Page"

app.include_router(route.router, prefix="/board", tags=["Board"])
