from typing import List
from fastapi import APIRouter, HTTPException, Depends, Header
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import PinSchema, RequestPin, RequestFavoritePin
import crud
from models import Pin, Tag, FavoritePin

router_pin = APIRouter(
    prefix="/pin",
    tags=["pin"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router_pin.post("/create")
async def create_pin(pin_data: PinSchema, db: Session = Depends(get_db), authorization: str = Header(None)):
    try:
        _, token = authorization.split("Bearer ")
        user_id = int(token)
        db_pin = Pin(
            title=pin_data.title,
            image_id=pin_data.image_id,
            description=pin_data.description,
            user_id=user_id,
            board_id=pin_data.board_id,
            tags=[]
        )

        db.add(db_pin)
        db.commit()

        tag_names = pin_data.tags.split(',')

        for tag_name in tag_names:
            tag_name = tag_name.strip()
            if tag_name:
                db_tag = db.query(Tag).filter(Tag.name == tag_name).first()
                if not db_tag:
                    db_tag = Tag(name=tag_name)
                    db.add(db_tag)
                    db.commit()
                    db.refresh(db_tag)
                db_pin.tags.append(db_tag)

        db.commit()

        print("Pin created successfully")
        return {"message": "Pin created successfully"}

    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
    finally:
        pass

# @router_pin.post('/create')
# async def create(request: RequestPin, db: Session = Depends(get_db)):
#     return crud.create_pin(db, request.parameter)


@router_pin.get('/')
async def get(db: Session = Depends(get_db)):
    return crud.get_all(db, Pin, 0, 100)


@router_pin.get('/{id}')
async def get_by_id(id: int, db: Session = Depends(get_db)):
    return crud.get_by_id(db, Pin, id)


@router_pin.post("/update")
async def update(request: RequestPin, db: Session = Depends(get_db)):
    return crud.update_pin(db, Pin, object_id=request.parameter.id, image=request.parameter.image, description=request.parameter.description)


@router_pin.delete("/delete/{id}")
async def delete(id: int, db: Session = Depends(get_db)):
    return crud.remove(db, Pin, id)


@router_pin.get("/pin_tags/{id}")
async def get_tags_for_pin(id: int, db: Session = Depends(get_db)):
    return crud.get_tags_for_pin(db, id)


@router_pin.post("/pin_sort_by_tags/")
async def pins_sort_by_tags(tags: List[str], db: Session = Depends(get_db)):
    return crud.pins_sort_by_tags(db, tags)


@router_pin.post("/add_to_favorite_pin/")
async def add_pin_to_favorite(request: RequestFavoritePin, db: Session = Depends(get_db)):
    pin_id = request.parameter.pin_id
    user_id = request.parameter.user_id
    favorite_pin = FavoritePin(pin_id=pin_id, user_id=user_id)
    db.add(favorite_pin)
    db.commit()
    db.refresh(favorite_pin)
    return favorite_pin


@router_pin.get("/get_all_user_pins/{user_id}")
async def get_all_user_pins(user_id: int, db: Session = Depends(get_db)):
    pins = db.query(Pin).filter(Pin.user_id == user_id).all()
    return pins


@router_pin.post("/get_favorite_pin_for_user/{user_id}")
async def get_favorite_pin_for_user(user_id: int, db: Session = Depends(get_db)):
    favorite_pins = db.query(FavoritePin).filter(FavoritePin.user_id == user_id).all()
    return favorite_pins


@router_pin.post("/pins_sort_by_board/{board_id}")
async def pins_sort_by_board(board_id: int, db: Session = Depends(get_db)):
    pins = db.query(Pin).filter(Pin.board_id == board_id).all()
    return pins


@router_pin.delete("/remove_favorite_pin/{favorite_pin_id}")
async def remove_favorite_pin(favorite_pin_id: int, db: Session = Depends(get_db)):
    return crud.remove(db, FavoritePin, favorite_pin_id)
