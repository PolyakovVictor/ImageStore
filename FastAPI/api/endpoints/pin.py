from typing import List
from fastapi import APIRouter, HTTPException, Depends, Header
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import PinSchema, RequestPin
import crud
from models import Pin, Tag

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
async def create_pin(pin_data: PinSchema, Session=Depends(get_db), authorization: str = Header(None)):
    try:
        # Создать объект Image
        _, token = authorization.split("Bearer ")
        user_id = int(token)
        print("fastapi test Authorization: ", user_id)
        db_pin = Pin(
            title=pin_data.title,
            image_id=pin_data.image_id,
            description=pin_data.description,
            user_id=user_id,
            board_id=pin_data.board_id,
            tags=[]
        )

        Session.add(db_pin)

        # Сохранить объекты в базе данных

        Session.commit()

        # Добавить теги к пину

        tag_names = pin_data.tags.split(',')

        for tag_name in tag_names:
            tag_name = tag_name.strip()
            if tag_name:
                db_tag = Session.query(Tag).filter(Tag.name == tag_name).first()
                if not db_tag:
                    db_tag = Tag(name=tag_name)
                    Session.add(db_tag)
                    Session.commit()
                    Session.refresh(db_tag)
                db_pin.tags.append(db_tag)

        # Сохранить изменения в базе данных

        Session.commit()

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


@router_pin.post("/delete/{id}")
async def delete(id: int, db: Session = Depends(get_db)):
    return crud.remove(db, Pin, id)


@router_pin.get("/pin_tags/{id}")
async def get_tags_for_pin(id: int, db: Session = Depends(get_db)):
    return crud.get_tags_for_pin(db, id)


@router_pin.post("/pin_sort_by_tags/")
async def pins_sort_by_tags(tags: List[str], db: Session = Depends(get_db)):
    return crud.pins_sort_by_tags(db, tags)
