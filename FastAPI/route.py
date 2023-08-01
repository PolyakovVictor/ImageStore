from fastapi import APIRouter, HTTPException, Path, Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import BoardSchema, PinSchema, RequestBoard, Response
import crud

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/create')
async def create(request: RequestBoard, db: Session = Depends(get_db)):
    return crud.create_board(db, request.parameter)


@router.get('/')
async def get(db: Session = Depends(get_db)):
    return crud.get_board(db, 0, 100)


@router.get('/{id}')
async def get_by_id(id: int, db: Session = Depends(get_db)):
    return crud.get_board_by_id(db, id)


@router.post("/update")
async def update(request: RequestBoard, db: Session = Depends(get_db)):
    return crud.update_board(db, board_id=request.parameter.id, title=request.parameter.title, description=request.parameter.description)


@router.post("/{id}")
async def delete(id: int, db: Session = Depends(get_db)):
    return crud.remove_board(db, board_id=id)
