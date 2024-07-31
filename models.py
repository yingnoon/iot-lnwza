from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship

from database import Base

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    year = Column(Integer, index=True)
    is_published = Column(Boolean, index=True)
    detail = Column(String, index=True)
    summary = Column(String, index=True)
    group = Column(String, index=True)

class Info(Base):
    __tablename__ = 'Info'

    firstname = Column(String, index=True)
    surname = Column(String, index=True)
    id = Column(String, primary_key=True, index=True)
    birth = Column(String, index=True)
    gender = Column(String, index=True)

class Menu(Base):
    __tablename__ = 'menu'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Integer, index=True)
    detail = Column(String, index=True)
    
class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Integer, index=True)
    total = Column(Integer, index=True)
    note = Column(String, index=True)

