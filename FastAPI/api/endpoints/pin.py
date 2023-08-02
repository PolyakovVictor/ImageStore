from fastapi import APIRouter, HTTPException, Path, Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import BoardSchema, PinSchema, RequestPin, RequestBoard, Response
import crud
from models import Pin

router_pin = APIRouter(
    prefix="/Pin",
    tags=["pin"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router_pin.post('/create')
async def create(request: RequestPin, db: Session = Depends(get_db)):
    return crud.create_pin(db, request.parameter)


@router_pin.get('/')
async def get(db: Session = Depends(get_db)):
    return crud.get_all(db, Pin, 0, 100)


@router_pin.get('/{id}')
async def get_by_id(id: int, db: Session = Depends(get_db)):
    return crud.get_by_id(db, Pin, id)


@router_pin.post("/update")
async def update(request: RequestPin, db: Session = Depends(get_db)):
    return crud.update_pin(db, Pin, object_id=request.parameter.id, image_url=request.parameter.image_url, description=request.parameter.description)


@router_pin.post("/delete/{id}")
async def delete(id: int, db: Session = Depends(get_db)):
    return crud.remove(db, Pin, id)
