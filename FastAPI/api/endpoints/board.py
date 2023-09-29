from fastapi import APIRouter, HTTPException, Path, Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import BoardSchema, PinSchema, RequestBoard, Response
import crud
from models import Board, Pin

router_board = APIRouter(
    prefix="/board",
    tags=["Board"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router_board.post('/create')
async def create(request: RequestBoard, db: Session = Depends(get_db)):
    return crud.create_board(db, request.parameter)


@router_board.get('/')
async def get(db: Session = Depends(get_db)):
    return crud.get_all(db, Board, 0, 100)


@router_board.get('/{id}')
async def get_by_id(id: int, db: Session = Depends(get_db)):
    return crud.get_by_id(db, Board, id)


@router_board.get("/get_all_user_boards/{user_id}")
async def get_all_user_boards(user_id: int, db: Session = Depends(get_db)):
    boards = db.query(Board).filter(Board.owner_id == user_id).all()
    return boards


@router_board.post("/update")
async def update(request: RequestBoard, db: Session = Depends(get_db)):
    return crud.update_board(db, board_id=request.parameter.id, title=request.parameter.title, description=request.parameter.description)


@router_board.delete("/delete/{id}")
async def delete(id: int, db: Session = Depends(get_db)):
    return crud.remove(db, Board, id)
