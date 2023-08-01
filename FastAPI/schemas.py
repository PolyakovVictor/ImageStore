from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar('T')


class BoardSchema(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    owner_id: Optional[int] = None

    class Config:
        from_attributes = True


class PinSchema(BaseModel):
    __tablename__ = "pins"
    id: Optional[int] = None
    image_url: Optional[str] = None
    description: Optional[str] = None
    board_id: Optional[str] = None

    class Config:
        from_attributes = True


class RequestBoard(BaseModel):
    parameter: BoardSchema = Field(...)


class Response(BaseModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]
