from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


pin_tags = Table(
    'pin_tags', Base.metadata,
    Column('pin_id', Integer, ForeignKey('pin.id')),
    Column('tag_id', Integer, ForeignKey('tag.id'))
)


class Board(Base):
    __tablename__ = "boards"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, index=True)

    # Отношение доски к её пинам
    pins = relationship("Pin", back_populates="board")


class Pin(Base):
    __tablename__ = "pin"
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, index=True)
    description = Column(String, index=True)
    board_id = Column(Integer, ForeignKey("boards.id"))
    tags = relationship("Tag", secondary=pin_tags, back_populates="pins")
    board = relationship("Board", back_populates="pins")


class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    pins = relationship("Pin", secondary=pin_tags, back_populates="tags")
