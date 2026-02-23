# pylint: disable=too-few-public-methods

from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from .sqlite import Base

class Trainer(Base):
    """
        Class representing a pokemon trainer
    """
    __tablename__ = "trainers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    birthdate = Column(Date)

    inventory = relationship("Item", back_populates="trainer")
    pokemons = relationship("Pokemon", back_populates="trainer")

class Pokemon(Base):
    """
        Class representing a pokemon
        Parameters:
            api_id (int): id from the pokeapi
            name (str): Populate with the pokeapi data 
    """
    __tablename__ = "pokemons"

    id = Column(Integer, primary_key=True, index=True)
    api_id = Column(Integer, index=True)
    name = Column(String, index=True)
    custom_name = Column(String, index=True)
    trainer_id = Column(Integer, ForeignKey("trainers.id"))

    trainer = relationship("Trainer", back_populates="pokemons")

class Item(Base):
    """
        Class representing a pokemon trainer
    """
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    trainer_id = Column(Integer, ForeignKey("trainers.id"))

    trainer = relationship("Trainer", back_populates="inventory")
