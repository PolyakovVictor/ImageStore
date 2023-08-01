from sqlalchemy.orm import Session
from models import Board, Pin
from schemas import BoardSchema


def get_board(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Board).offset(skip).limit(limit).all()


def get_board_by_id(db: Session, board_id: int):
    return db.query(Board).filter(Board.id == board_id).first()


def create_board(db: Session, board: BoardSchema):
    _board = Board(title=board.title, description=board.description, owner_id=board.owner_id)
    db.add(_board)
    db.commit()
    db.refresh(_board)
    return _board


def remove_board(db: Session, board_id: int):
    _board = get_board_by_id(db=db, board_id=board_id)
    db.delete(_board)
    db.commit()


def update_board(db: Session, board_id: int, title: str, description: str):
    _board = get_board_by_id(db=db, board_id=board_id)
    _board.title = title if title else _board.title
    _board.description = description if description else _board.description
    db.commit()
    db.refresh(_board)
    return _board
