import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_pokemons_empty():
    # Act
    response = client.get("/pokemons/")

    # Assert
    assert response.status_code == 200
    assert response.json() == []


def test_get_pokemons_after_assignment(mocker):
    # Arrange
    trainer_id = client.post(
        "/trainers/", json={"name": "Ash", "birthdate": "1997-04-01"}
    ).json()["id"]
    mocker.patch("app.actions.get_pokemon_name", return_value="pikachu")
    client.post(f"/trainers/{trainer_id}/pokemon/", json={"api_id": 25})

    # Act
    response = client.get("/pokemons/")

    # Assert
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "pikachu"


def test_get_pokemons_all_trainers(mocker):
    # Arrange
    ash_id = client.post(
        "/trainers/", json={"name": "Ash", "birthdate": "1997-04-01"}
    ).json()["id"]
    misty_id = client.post(
        "/trainers/", json={"name": "Misty", "birthdate": "1997-11-15"}
    ).json()["id"]
    mocker.patch("app.actions.get_pokemon_name", return_value="pikachu")
    client.post(f"/trainers/{ash_id}/pokemon/", json={"api_id": 25})
    mocker.patch("app.actions.get_pokemon_name", return_value="starmie")
    client.post(f"/trainers/{misty_id}/pokemon/", json={"api_id": 121})

    # Act
    response = client.get("/pokemons/")

    # Assert
    assert response.status_code == 200
    names = [p["name"] for p in response.json()]
    assert "pikachu" in names
    assert "starmie" in names


def test_get_pokemons_limit(mocker):
    # Arrange
    trainer_id = client.post(
        "/trainers/", json={"name": "Gary", "birthdate": "1997-04-01"}
    ).json()["id"]

    for api_id, name in [(1, "bulbasaur"), (4, "charmander"), (7, "squirtle")]:
        mocker.patch("app.actions.get_pokemon_name", return_value=name)
        client.post(f"/trainers/{trainer_id}/pokemon/", json={"api_id": api_id})

    # Act
    response = client.get("/pokemons/?skip=0&limit=2")

    # Assert
    assert response.status_code == 200
    assert len(response.json()) == 2


pokemon_data = [(25, "pikachu"), (1, "bulbasaur"), (150, "mewtwo")]


@pytest.mark.parametrize("api_id, name", pokemon_data)
def test_pokemon_in_global_list_parametrized(mocker, api_id, name):
    # Arrange
    mocker.patch("app.actions.get_pokemon_name", return_value=name)
    trainer_id = client.post(
        "/trainers/", json={"name": f"Trainer_{api_id}", "birthdate": "2000-01-01"}
    ).json()["id"]
    client.post(f"/trainers/{trainer_id}/pokemon/", json={"api_id": api_id})

    # Act
    response = client.get("/pokemons/")

    # Assert
    assert response.status_code == 200
    all_names = [p["name"] for p in response.json()]
    assert name in all_names
