from sqlalchemy.orm import Session
from models import Board, Pin
from schemas import BoardSchema, PinSchema


def get_all(db: Session, object: BoardSchema, skip: int = 0, limit: int = 100):
    return db.query(object).offset(skip).limit(limit).all()


def get_by_id(db: Session, object: Board, object_id: int):
    return db.query(object).filter(object.id == object_id).first()


def remove(db: Session, object: Board, object_id: int):
    _object = get_by_id(db=db, object=object, object_id=object_id)
    db.delete(_object)
    db.commit()


def update_board(db: Session, object_id: int, title: str, description: str):
    _board = get_by_id(db=db, object_id=object_id)
    _board.title = title if title else _board.title
    _board.description = description if description else _board.description
    db.commit()
    db.refresh(_board)
    return _board


def update_pin(db: Session, object: PinSchema, object_id: int, image_url: str, description: str):
    _pin = get_by_id(db=db, object=object, object_id=object_id)
    _pin.image_url = image_url if image_url else _pin.image_url
    _pin.description = description if description else _pin.description
    db.commit()
    db.refresh(_pin)
    return _pin


def create_board(db: Session, object: BoardSchema):
    _board = Board(title=object.title, description=object.description, owner_id=object.owner_id)
    db.add(_board)
    db.commit()
    db.refresh(_board)
    return _board


def create_pin(db: Session, object: PinSchema):
    _pin = Pin(image_url=object.image_url, description=object.description, board_id=object.board_id)
    db.add(_pin)
    db.commit()
    db.refresh(_pin)
    return _pin
