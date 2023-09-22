from datetime import datetime
from fastapi import APIRouter, Depends, UploadFile, File
from config import SessionLocal
from sqlalchemy.orm import Session
import crud
from models import Image

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
async def upload_image(file: UploadFile = File(...), Session=Depends(get_db)):

    # unique_filename = str(uuid.uuid4())

    # original_filename = 'example.jpg'
    # file_extension = original_filename.split('.')[-1]

    # new_filename = f"{unique_filename}.{file_extension}"

    with open(f"../Django/ImageStore/imageStoreApp/static/images/{file.filename}", "wb") as f:
        f.write(file.file.read())

    image = Image(name=file.filename, size=file.size, modified_at=datetime.now(), type=file.content_type)
    Session.add(image)
    Session.commit()

    return image.id


@router_image.get('/')
async def get(db: Session = Depends(get_db)):
    return crud.get_all(db, Image, 0, 100)


@router_image.get('/{id}')
async def get_by_id(id: int, db: Session = Depends(get_db)):
    return crud.get_by_id(db, Image, id)
