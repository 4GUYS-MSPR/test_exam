import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_get_items_empty():
    # Act
    response = client.get("/items/")

    # Assert
    assert response.status_code == 200
    assert response.json() == []


def test_get_items_after_creation():
    # Arrange
    trainer_id = client.post(
        "/trainers/", json={"name": "Ash", "birthdate": "1997-04-01"}
    ).json()["id"]
    client.post(
        f"/trainers/{trainer_id}/item/",
        json={"name": "Potion", "description": "Heals 20 HP"},
    )

    # Act
    response = client.get("/items/")

    # Assert
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Potion"


def test_get_items_all_trainers():
    # Arrange
    ash_id = client.post(
        "/trainers/", json={"name": "Ash", "birthdate": "1997-04-01"}
    ).json()["id"]
    misty_id = client.post(
        "/trainers/", json={"name": "Misty", "birthdate": "1997-11-15"}
    ).json()["id"]

    client.post(
        f"/trainers/{ash_id}/item/",
        json={"name": "Potion", "description": "Heals 20 HP"},
    )
    client.post(
        f"/trainers/{misty_id}/item/",
        json={"name": "Master Ball", "description": "Never fails"},
    )

    # Act
    response = client.get("/items/")

    # Assert
    assert response.status_code == 200
    names = [i["name"] for i in response.json()]
    assert "Potion" in names
    assert "Master Ball" in names


def test_item_description_can_be_null():
    # Arrange
    trainer_id = client.post(
        "/trainers/", json={"name": "Gary", "birthdate": "1997-04-01"}
    ).json()["id"]
    client.post(f"/trainers/{trainer_id}/item/", json={"name": "Rare Candy"})

    # Act
    response = client.get("/items/")

    # Assert
    assert response.status_code == 200
    assert response.json()[0]["name"] == "Rare Candy"
    assert response.json()[0]["description"] is None


def test_get_items_limit():
    # Arrange
    trainer_id = client.post(
        "/trainers/", json={"name": "Red", "birthdate": "1996-01-01"}
    ).json()["id"]

    for name in ["Potion", "Super Potion", "Hyper Potion", "Max Potion"]:
        client.post(
            f"/trainers/{trainer_id}/item/",
            json={"name": name, "description": "A healing item"},
        )

    # Act
    response = client.get("/items/?skip=0&limit=2")

    # Assert
    assert response.status_code == 200
    assert len(response.json()) == 2


item_data = [
    ("Potion", "Heals 20 HP"),
    ("Super Potion", "Heals 50 HP"),
    ("Hyper Potion", "Heals 200 HP"),
]


@pytest.mark.parametrize("item_name, description", item_data)
def test_item_in_global_list_parametrized(item_name, description):
    # Arrange
    trainer_id = client.post(
        "/trainers/", json={"name": f"Trainer_{item_name}", "birthdate": "2000-01-01"}
    ).json()["id"]
    client.post(
        f"/trainers/{trainer_id}/item/",
        json={"name": item_name, "description": description},
    )

    # Act
    response = client.get("/items/")

    # Assert
    assert response.status_code == 200
    all_names = [i["name"] for i in response.json()]
    assert item_name in all_names
