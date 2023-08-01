from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


# Модель доски (board)
class Board(Base):
    __tablename__ = "boards"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, index=True)

    # Отношение доски к её пинам
    pins = relationship("Pin", back_populates="board")


# Модель пина (pin)
class Pin(Base):
    __tablename__ = "pins"
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, index=True)
    description = Column(String, index=True)
    board_id = Column(Integer, ForeignKey("boards.id"))

    # Отношение пина к его доске
    board = relationship("Board", back_populates="pins")
