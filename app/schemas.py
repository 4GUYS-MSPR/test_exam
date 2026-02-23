# pylint: disable=too-few-public-methods

from datetime import date
from typing import  List, Optional, Union
from pydantic import BaseModel

#
#  ITEM
#
class ItemBase(BaseModel):
    name: str
    description: Union[str, None] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    trainer_id: int

    class Config:
        orm_mode = True

#
#  POKEMON
#
class PokemonBase(BaseModel):
    api_id: int
    custom_name: Optional[str] = None

class PokemonCreate(PokemonBase):
    pass

class Pokemon(PokemonBase):
    id: int
    name: str
    trainer_id: int

    class Config:
        orm_mode = True

    
        
class PokemonFight(BaseModel):
    first_pokemon_id: int
    second_pokemon_id: int

class PokemonFightResult(BaseModel):
    winner: Optional[str] = None
    draw: bool = False

#  TRAINER
#
class TrainerBase(BaseModel):
    name: str
    birthdate: date

class TrainerCreate(TrainerBase):
    pass

class Trainer(TrainerBase):
    id: int
    inventory: List[Item] = []
    pokemons: List[Pokemon] = []

    class Config:
        orm_mode = True
