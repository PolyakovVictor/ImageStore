from datetime import datetime
from fastapi import APIRouter, HTTPException, Path, Depends, UploadFile, File
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import BoardSchema, PinSchema, RequestBoard, Response
import crud
from models import Board, Pin, Image

router_image = APIRouter(
    prefix="/image",
    tags=["Image"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router_image.post("/upload")
async def upload_image(file: UploadFile = File(...), Session = Depends(get_db)):
  # Получить имя файла
  name = file.filename

  # Сохранить изображение в локальную папку
  with open(f"images/{name}", "wb") as f:
    f.write(file.file.read())

  # Добавить изображение в базу данных
    image = Image(name=name, size=file.size, modified_at=datetime.now(), type=file.content_type)
    Session.add(image)
    Session.commit()
    print("IMAGE ID: ", image.id)

  return image.id


@router_image.get('/')
async def get(db: Session = Depends(get_db)):
    return crud.get_all(db, Image, 0, 100)
