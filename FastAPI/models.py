from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
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

    pins = relationship("Pin", back_populates="board")


class Pin(Base):
    __tablename__ = "pin"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    image_id = Column(Integer, ForeignKey("images.id"))
    description = Column(String, index=True)
    board_id = Column(Integer, ForeignKey("boards.id"))

    image = relationship("Image", back_populates="pins")
    tags = relationship("Tag", secondary=pin_tags, back_populates="pins")
    board = relationship("Board", back_populates="pins")


class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    pins = relationship("Pin", secondary=pin_tags, back_populates="tags")


class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    size = Column(Integer)
    type = Column(String(255))
    modified_at = Column(DateTime)

    pins = relationship("Pin", back_populates="image")

    def __repr__(self):
        return f"Image(id={self.id}, name={self.name}, size={self.size}, type={self.type}, modified_at={self.modified_at})"
