from sqlalchemy.orm import Session
from models import Board, Pin, Tag
from schemas import BoardSchema, PinSchema, TagSchema


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


def update_pin(db: Session, object: PinSchema, object_id: int, image: str, description: str):
    _pin = get_by_id(db=db, object=object, object_id=object_id)
    _pin.image = image if image else _pin.image
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


# def create_pin(db: Session, pin: PinSchema):
#     tag_ids = pin.tag_id
#     pin_db = Pin(**pin.model_dump(exclude={"tag_id", "id"}))
#     for tag_id in tag_ids:
#         tag = db.query(Tag).filter(Tag.id == tag_id).first()
#         if tag:
#             pin_db.tags.append(tag)
#     db.add(pin_db)
#     db.commit()
#     db.refresh(pin_db)
#     return pin_db


def get_tags_for_pin(db: Session, pin_id: int):
    pin = db.query(Pin).get(pin_id)
    if pin:
        return pin.tags
    return []


def pins_sort_by_tags(db: Session, tags: list[str]):
    pins_with_tags = (db.query(Pin).join(Pin.tags).filter(Tag.name.in_(tags)).all())
    if pins_with_tags:
        return pins_with_tags
    return []


def create_tag(db: Session, object: TagSchema):
    _tag = Tag(name=object.name)
    db.add(_tag)
    db.commit()
    db.refresh(_tag)
    return _tag
