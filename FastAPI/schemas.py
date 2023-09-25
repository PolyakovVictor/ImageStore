from typing import Optional, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar('T')


class BoardSchema(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    owner_id: Optional[int] = None

    class Config:
        from_attributes = True


class TagSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class PinSchema(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[str] = None
    user_id: Optional[int] = None
    image_id: Optional[int] = None
    board_id: Optional[int] = None

    class Config:
        from_attributes = True


class FavoritePinSchema(BaseModel):
    user_id: int
    pin_id: int

    class Config:
        from_attributes = True


class RequestFavoritePin(BaseModel):
    parameter: FavoritePinSchema = Field(...)


class RequestBoard(BaseModel):
    parameter: BoardSchema = Field(...)


class RequestPin(BaseModel):
    parameter: PinSchema = Field(...)


class RequestTag(BaseModel):
    parameter: TagSchema = Field(...)



class Response(BaseModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]
