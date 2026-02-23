from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter,  Depends
from app import actions, schemas
from app.utils.utils import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Pokemon])
def get_pokemons(skip: int = 0, limit: int = 100, database: Session = Depends(get_db)):
    """
        Return all pokemons
        Default limit is 100
    """
    pokemons = actions.get_pokemons(database, skip=skip, limit=limit)
    return pokemons

@router.get("/random/", response_model=List[schemas.PokemonWithStats])
def get_random_pokemons(limit: int = 100, database: Session = Depends(get_db)):
    """
        Return 3 random pokemons
        Default limit is 3
    """
    pokemons = actions.get_random_pokemons(database, limit=limit)
    return pokemons

@router.get("/fight", response_model=schemas.PokemonFightResult)
def fight_pokemons(first_pokemon_id: int, second_pokemon_id: int,
                   database: Session = Depends(get_db)):
    """
        Return result of the fight
    """
    return actions.fight_pokemons(database, first_pokemon_id, second_pokemon_id)
