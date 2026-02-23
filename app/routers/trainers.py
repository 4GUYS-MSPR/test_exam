from typing import List
from sqlalchemy.orm import Session

from fastapi import APIRouter,  Depends, HTTPException

from app.utils.utils import get_db
from app import actions, schemas

router = APIRouter()

@router.post("/", response_model=schemas.Trainer)
def create_trainer(trainer: schemas.TrainerCreate, database: Session = Depends(get_db)):
    """
        Create a trainer
    """
    return actions.create_trainer(database=database, trainer=trainer)


@router.get("", response_model=List[schemas.Trainer])
def get_trainers(skip: int = 0, limit: int = 100, database: Session = Depends(get_db)):
    """
        Return all trainers
        Default limit is 100
    """
    trainers = actions.get_trainers(database, skip=skip, limit=limit)
    return trainers


@router.get("/{trainer_id}", response_model=schemas.Trainer)
def get_trainer(trainer_id: int, database: Session = Depends(get_db)):
    """
        Return trainer from his id
    """
    db_trainer = actions.get_trainer(database, trainer_id=trainer_id)
    if db_trainer is None:
        raise HTTPException(status_code=404, detail="Trainer not found")
    return db_trainer


@router.post("/{trainer_id}/item/", response_model=schemas.Item)
def create_item_for_trainer(
    trainer_id: int, item: schemas.ItemCreate, database: Session = Depends(get_db)
):
    """
        Add an item in trainer inventory
    """
    return actions.add_trainer_item(database=database, item=item, trainer_id=trainer_id)


@router.post("/{trainer_id}/pokemon/", response_model=schemas.Pokemon)
def create_pokemon_for_trainer(
    trainer_id: int, pokemon: schemas.PokemonCreate, database: Session = Depends(get_db)
):
    """
        Add a Pokemon to a trainer
    """
    return actions.add_trainer_pokemon(database=database, pokemon=pokemon, trainer_id=trainer_id)
