from fastapi import APIRouter, HTTPException, Path, Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import RequestTag
import crud
from models import Tag

router_tag = APIRouter(
    prefix="/tag",
    tags=["tag"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router_tag.post('/create')
async def create(request: RequestTag, db: Session = Depends(get_db)):
    return crud.create_tag(db, request.parameter)


@router_tag.get('/')
async def get(db: Session = Depends(get_db)):
    return crud.get_all(db, Tag, 0, 100)


@router_tag.get('/{id}')
async def get_by_id(id: int, db: Session = Depends(get_db)):
    return crud.get_by_id(db, Tag, id)


@router_tag.post("/delete/{id}")
async def delete(id: int, db: Session = Depends(get_db)):
    return crud.remove(db, Tag, id)
