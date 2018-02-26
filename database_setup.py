import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    """User table class

    Attributes:
        id: a unique identifier for the system user
        name: the user's name
        email: the user's email address
    """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)


class Category(Base):
    """Category table class

    Attributes:
        id: a unique identifier for the category
        name: the category's name
    """
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
        }


class Item(Base):
    """Item table class

    Attributes:
        name: the item's name
        id: a unique identifier for the item
        description: a description of the item
        cat_id: the category.id of the related category
        category: the related category
        user_id: the user_id of the user who created the item
        user: the user who created the item
    """
    __tablename__ = 'item'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    cat_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'cat_id': self.cat_id,
        }


engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
