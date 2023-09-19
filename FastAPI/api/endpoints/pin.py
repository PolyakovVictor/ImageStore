from fastapi import APIRouter, HTTPException, Path, Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import BoardSchema, PinSchema, RequestPin, RequestBoard, Response
import crud
import base64
from models import Pin, Tag

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


@router_pin.post("/create")
async def create_pin(pin_data: PinSchema, Session = Depends(get_db)):
    try:
        if pin_data.image != None:
            image_bits = base64.b64decode(pin_data.image.encode('utf-8'))
            db_pin = Pin(
                title=pin_data.title,
                image=image_bits,
                description=pin_data.description,
                board_id=pin_data.board_id,
                tags=[]
            )
        else:
            db_pin = Pin(
                title=pin_data.title,
                description=pin_data.description,
                board_id=pin_data.board_id,
                tags=[]
            )
        Session.add(db_pin)
        Session.commit()
        Session.refresh(db_pin)
        
        print("in if")
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
