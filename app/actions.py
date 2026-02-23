import random

from sqlalchemy.orm import Session

from . import models, schemas
from .utils.pokeapi import battle_compare_stats, get_pokemon_name, get_pokemon_stats

def get_trainer(database: Session, trainer_id: int):
    """
        Find a user by his id
    """
    return database.query(models.Trainer).filter(models.Trainer.id == trainer_id).first()


def get_trainer_by_name(database: Session, name: str):
    """
        Find a user by his name
    """
    return database.query(models.Trainer).filter(models.Trainer.name == name).all()


def get_trainers(database: Session, skip: int = 0, limit: int = 100):
    """
        Find all users
        Default limit is 100
    """
    return database.query(models.Trainer).offset(skip).limit(limit).all()


def create_trainer(database: Session, trainer: schemas.TrainerCreate):
    """
        Create a new trainer
    """
    db_trainer = models.Trainer(name=trainer.name, birthdate=trainer.birthdate)
    database.add(db_trainer)
    database.commit()
    database.refresh(db_trainer)
    return db_trainer


def add_trainer_pokemon(database: Session, pokemon: schemas.PokemonCreate, trainer_id: int):
    """
        Create a pokemon and link it to a trainer
    """
    db_item = models.Pokemon(
        **pokemon.dict(), name=get_pokemon_name(pokemon.api_id), trainer_id=trainer_id)
    database.add(db_item)
    database.commit()
    database.refresh(db_item)
    return db_item


def add_trainer_item(database: Session, item: schemas.ItemCreate, trainer_id: int):
    """
        Create an item and link it to a trainer
    """
    db_item = models.Item(**item.dict(), trainer_id=trainer_id)
    database.add(db_item)
    database.commit()
    database.refresh(db_item)
    return db_item


def get_items(database: Session, skip: int = 0, limit: int = 100):
    """
        Find all items
        Default limit is 100
    """
    return database.query(models.Item).offset(skip).limit(limit).all()


def get_pokemon(database: Session, pokemon_id: int):
    """
        Find a pokemon by his id
    """
    return database.query(models.Pokemon).filter(models.Pokemon.id == pokemon_id).first()


def get_pokemons(database: Session, skip: int = 0, limit: int = 100):
    """
        Find all pokemons
        Default limit is 100
    """
    return database.query(models.Pokemon).offset(skip).limit(limit).all()

def fight_pokemons(database: Session, first_pokemon_id: int, second_pokemon_id: int):
    """
        Fait s'affronter 2 pokémons
    """
    first_pokemon = get_pokemon(database, first_pokemon_id)
    second_pokemon = get_pokemon(database, second_pokemon_id)

    battle_result = battle_compare_stats(
        get_pokemon_stats(first_pokemon.api_id),
        get_pokemon_stats(second_pokemon.api_id),
    )

    winner = None
    if battle_result > 0:
        winner = first_pokemon
    elif battle_result < 0:
        winner = second_pokemon

    return schemas.PokemonFightResult(winner=winner.custom_name, draw=winner is None)

def get_random_pokemons(database : Session, limit: int = 100):
    """
        Select 3 random pokemons in db and return informations
        Default limit is 3
    """
    count = len(database.query(models.Pokemon).limit(limit).all())
    pokemons = database.query(models.Pokemon).limit(limit).all()
    random_pokemon = []
    while len(random_pokemon) < 3:
        number = random.randint(1, count) -1
        if pokemons[number] in random_pokemon:
            continue
        else:
            random_pokemon.append(pokemons[number])
    return random_pokemon
