import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


# ---------------------------------------------------------------------------
# POST /trainers/
# ---------------------------------------------------------------------------


def test_create_trainer():
    # Arrange
    payload = {"name": "Ash Ketchum", "birthdate": "1997-04-01"}

    # Act
    response = client.post("/trainers/", json=payload)

    # Assert
    assert response.status_code == 200
    assert response.json()["name"] == "Ash Ketchum"


def test_create_trainer_returns_id():
    # Arrange
    payload = {"name": "Misty", "birthdate": "1997-11-15"}

    # Act
    response = client.post("/trainers/", json=payload)

    # Assert
    assert response.status_code == 200
    assert "id" in response.json()


def test_create_trainer_has_empty_collections():
    # Arrange
    payload = {"name": "Brock", "birthdate": "1995-09-03"}

    # Act
    response = client.post("/trainers/", json=payload)

    # Assert
    assert response.json()["inventory"] == []
    assert response.json()["pokemons"] == []


trainer_names = ["Trainer_Ash", "Trainer_Misty", "Trainer_Brock"]


@pytest.mark.parametrize("name", trainer_names)
def test_create_trainer_parametrized(name):
    # Arrange
    payload = {"name": name, "birthdate": "2000-01-01"}

    # Act
    response = client.post("/trainers/", json=payload)

    # Assert
    assert response.status_code == 200
    assert response.json()["name"] == name


# ---------------------------------------------------------------------------
# GET /trainers
# ---------------------------------------------------------------------------


def test_get_trainers_empty():
    # Act
    response = client.get("/trainers")

    # Assert
    assert response.status_code == 200
    assert response.json() == []


def test_get_trainers_after_creation():
    # Arrange
    client.post("/trainers/", json={"name": "Gary", "birthdate": "1997-04-01"})
    client.post("/trainers/", json={"name": "May", "birthdate": "2000-05-05"})

    # Act
    response = client.get("/trainers")

    # Assert
    assert response.status_code == 200
    names = [t["name"] for t in response.json()]
    assert "Gary" in names
    assert "May" in names


def test_get_trainers_limit():
    # Arrange
    for i in range(5):
        client.post(
            "/trainers/", json={"name": f"Player{i}", "birthdate": "2000-01-01"}
        )

    # Act
    response = client.get("/trainers?skip=0&limit=2")

    # Assert
    assert response.status_code == 200
    assert len(response.json()) == 2


# ---------------------------------------------------------------------------
# GET /trainers/{trainer_id}
# ---------------------------------------------------------------------------


def test_get_trainer_by_id():
    # Arrange
    trainer_id = client.post(
        "/trainers/", json={"name": "Dawn", "birthdate": "2001-01-01"}
    ).json()["id"]

    # Act
    response = client.get(f"/trainers/{trainer_id}")

    # Assert
    assert response.status_code == 200
    assert response.json()["name"] == "Dawn"


def test_get_trainer_not_found():
    # Act
    response = client.get("/trainers/99999")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Trainer not found"


# ---------------------------------------------------------------------------
# POST /trainers/{trainer_id}/item/
# ---------------------------------------------------------------------------


def test_add_item_to_trainer():
    # Arrange
    trainer_id = client.post(
        "/trainers/", json={"name": "Red", "birthdate": "1996-01-01"}
    ).json()["id"]

    # Act
    response = client.post(
        f"/trainers/{trainer_id}/item/",
        json={"name": "Potion", "description": "Heals 20 HP"},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["name"] == "Potion"
    assert response.json()["trainer_id"] == trainer_id


def test_item_appears_in_trainer_inventory():
    # Arrange
    trainer_id = client.post(
        "/trainers/", json={"name": "Leaf", "birthdate": "1997-07-07"}
    ).json()["id"]
    client.post(
        f"/trainers/{trainer_id}/item/",
        json={"name": "Super Potion", "description": "Heals 50 HP"},
    )

    # Act
    response = client.get(f"/trainers/{trainer_id}")

    # Assert
    item_names = [i["name"] for i in response.json()["inventory"]]
    assert "Super Potion" in item_names


item_names = ["Potion", "Super Potion", "Hyper Potion"]


@pytest.mark.parametrize("item_name", item_names)
def test_add_multiple_items_parametrized(item_name):
    # Arrange
    trainer_id = client.post(
        "/trainers/", json={"name": "Blue", "birthdate": "1996-01-01"}
    ).json()["id"]

    # Act
    response = client.post(
        f"/trainers/{trainer_id}/item/",
        json={"name": item_name, "description": "A healing item"},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["name"] == item_name


# ---------------------------------------------------------------------------
# POST /trainers/{trainer_id}/pokemon/
# ---------------------------------------------------------------------------


def test_add_pokemon_to_trainer(mocker):
    # Arrange
    mocker.patch("app.actions.get_pokemon_name", return_value="bulbasaur")
    trainer_id = client.post(
        "/trainers/", json={"name": "Erika", "birthdate": "1990-03-10"}
    ).json()["id"]

    # Act
    response = client.post(f"/trainers/{trainer_id}/pokemon/", json={"api_id": 1})

    # Assert
    assert response.status_code == 200
    assert response.json()["name"] == "bulbasaur"
    assert response.json()["trainer_id"] == trainer_id


def test_add_pokemon_with_custom_name(mocker):
    # Arrange
    mocker.patch("app.actions.get_pokemon_name", return_value="charmander")
    trainer_id = client.post(
        "/trainers/", json={"name": "Blaine", "birthdate": "1955-06-06"}
    ).json()["id"]

    # Act
    response = client.post(
        f"/trainers/{trainer_id}/pokemon/",
        json={"api_id": 4, "custom_name": "Flamie"},
    )

    # Assert
    assert response.json()["custom_name"] == "Flamie"
    assert response.json()["name"] == "charmander"


def test_pokemon_appears_in_trainer_pokemons(mocker):
    # Arrange
    mocker.patch("app.actions.get_pokemon_name", return_value="mewtwo")
    trainer_id = client.post(
        "/trainers/", json={"name": "Giovanni", "birthdate": "1960-10-18"}
    ).json()["id"]
    client.post(f"/trainers/{trainer_id}/pokemon/", json={"api_id": 150})

    # Act
    response = client.get(f"/trainers/{trainer_id}")

    # Assert
    pokemon_names = [p["name"] for p in response.json()["pokemons"]]
    assert "mewtwo" in pokemon_names


pokemon_ids = [(25, "pikachu"), (1, "bulbasaur"), (4, "charmander")]


@pytest.mark.parametrize("api_id, expected_name", pokemon_ids)
def test_add_pokemon_parametrized(mocker, api_id, expected_name):
    # Arrange
    mocker.patch("app.actions.get_pokemon_name", return_value=expected_name)
    trainer_id = client.post(
        "/trainers/", json={"name": f"Trainer_{api_id}", "birthdate": "2000-01-01"}
    ).json()["id"]

    # Act
    response = client.post(f"/trainers/{trainer_id}/pokemon/", json={"api_id": api_id})

    # Assert
    assert response.status_code == 200
    assert response.json()["name"] == expected_name
    assert response.json()["api_id"] == api_id
