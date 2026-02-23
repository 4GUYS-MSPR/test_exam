import pytest

from app.utils.pokeapi import (
    get_pokemon_data,
    get_pokemon_name,
    get_pokemon_stats,
    battle_pokemon,
    battle_compare_stats,
)


# ---------------------------------------------------------------------------
# get_pokemon_data
# ---------------------------------------------------------------------------

def test_get_pokemon_data_calls_correct_url(mocker):
    # Arrange
    mock_response = mocker.MagicMock()
    mock_response.json.return_value = {"name": "pikachu", "id": 25}
    mock_get = mocker.patch("app.utils.pokeapi.requests.get", return_value=mock_response)

    # Act
    result = get_pokemon_data(25)

    # Assert
    mock_get.assert_called_once_with(
        "https://pokeapi.co/api/v2/pokemon/25", timeout=10
    )
    assert result == {"name": "pikachu", "id": 25}


def test_get_pokemon_data_returns_parsed_json(mocker):
    # Arrange
    expected = {"name": "mewtwo", "id": 150}
    mock_response = mocker.MagicMock()
    mock_response.json.return_value = expected
    mocker.patch("app.utils.pokeapi.requests.get", return_value=mock_response)

    # Act
    result = get_pokemon_data(150)

    # Assert
    assert result == expected


pokemon_ids = [1, 4, 7, 25, 150]


@pytest.mark.parametrize("api_id", pokemon_ids)
def test_get_pokemon_data_parametrized(mocker, api_id):
    # Arrange
    mock_response = mocker.MagicMock()
    mock_response.json.return_value = {"name": f"pokemon_{api_id}", "id": api_id}
    mock_get = mocker.patch("app.utils.pokeapi.requests.get", return_value=mock_response)

    # Act
    result = get_pokemon_data(api_id)

    # Assert
    mock_get.assert_called_once_with(
        f"https://pokeapi.co/api/v2/pokemon/{api_id}", timeout=10
    )
    assert result["id"] == api_id


# ---------------------------------------------------------------------------
# get_pokemon_name
# ---------------------------------------------------------------------------

def test_get_pokemon_name_returns_name_field(mocker):
    # Arrange
    mocker.patch(
        "app.utils.pokeapi.get_pokemon_data",
        return_value={"name": "bulbasaur", "id": 1},
    )

    # Act
    result = get_pokemon_name(1)

    # Assert
    assert result == "bulbasaur"


def test_get_pokemon_name_calls_get_pokemon_data_with_correct_id(mocker):
    # Arrange
    mock_data = mocker.patch(
        "app.utils.pokeapi.get_pokemon_data",
        return_value={"name": "charmander"},
    )

    # Act
    get_pokemon_name(4)

    # Assert
    mock_data.assert_called_once_with(4)


pokemon_names = [(1, "bulbasaur"), (4, "charmander"), (7, "squirtle"), (25, "pikachu")]


@pytest.mark.parametrize("api_id, expected_name", pokemon_names)
def test_get_pokemon_name_parametrized(mocker, api_id, expected_name):
    # Arrange
    mocker.patch(
        "app.utils.pokeapi.get_pokemon_data",
        return_value={"name": expected_name},
    )

    # Act
    result = get_pokemon_name(api_id)

    # Assert
    assert result == expected_name


# ---------------------------------------------------------------------------
# get_pokemon_stats
# ---------------------------------------------------------------------------

def test_get_pokemon_stats_returns_stats(mocker):
    # Arrange
    expected_stats = [{"stat": {"name": "hp"}, "base_stat": 45}]
    mocker.patch(
        "app.utils.pokeapi.get_pokemon_data",
        return_value={"stats": expected_stats},
    )

    # Act
    result = get_pokemon_stats(1)

    # Assert
    assert result == expected_stats


stats_ids = [1, 25, 150, 999]


@pytest.mark.parametrize("api_id", stats_ids)
def test_get_pokemon_stats_parametrized(mocker, api_id):
    # Arrange
    expected_stats = [{"stat": {"name": "hp"}, "base_stat": api_id}]
    mocker.patch(
        "app.utils.pokeapi.get_pokemon_data",
        return_value={"stats": expected_stats},
    )

    # Act
    result = get_pokemon_stats(api_id)

    # Assert
    assert result == expected_stats


# ---------------------------------------------------------------------------
# battle_pokemon
# ---------------------------------------------------------------------------

def test_battle_pokemon_returns_draw(mocker):
    # Arrange
    pikachu = {"name": "pikachu", "id": 25}
    bulbasaur = {"name": "bulbasaur", "id": 1}
    mocker.patch("app.utils.pokeapi.get_pokemon_data", side_effect=[pikachu, bulbasaur])

    # Act
    result = battle_pokemon(25, 1)

    # Assert
    assert result == {"winner": "draw"}


def test_battle_pokemon_fetches_both_pokemons(mocker):
    # Arrange
    p1 = {"name": "squirtle", "id": 7}
    p2 = {"name": "eevee", "id": 133}
    mock_data = mocker.patch("app.utils.pokeapi.get_pokemon_data", side_effect=[p1, p2])

    # Act
    battle_pokemon(7, 133)

    # Assert
    assert mock_data.call_count == 2
    mock_data.assert_any_call(7)
    mock_data.assert_any_call(133)


battle_pairs = [(1, 4), (25, 150), (7, 133)]


@pytest.mark.parametrize("first_id, second_id", battle_pairs)
def test_battle_pokemon_always_draw_parametrized(mocker, first_id, second_id):
    # Arrange
    p1 = {"name": f"pokemon_{first_id}", "id": first_id}
    p2 = {"name": f"pokemon_{second_id}", "id": second_id}
    mocker.patch("app.utils.pokeapi.get_pokemon_data", side_effect=[p1, p2])

    # Act
    result = battle_pokemon(first_id, second_id)

    # Assert
    assert result == {"winner": "draw"}


# ---------------------------------------------------------------------------
# battle_compare_stats
# ---------------------------------------------------------------------------

def test_battle_compare_stats_first_wins():
    # Arrange
    strong = [{"stat": {"name": "hp"}, "base_stat": 100}, {"stat": {"name": "attack"}, "base_stat": 100}]
    weak   = [{"stat": {"name": "hp"}, "base_stat": 10},  {"stat": {"name": "attack"}, "base_stat": 10}]

    # Act
    result = battle_compare_stats(strong, weak)

    # Assert
    assert result == 1


def test_battle_compare_stats_second_wins():
    # Arrange
    weak   = [{"stat": {"name": "hp"}, "base_stat": 10},  {"stat": {"name": "attack"}, "base_stat": 10}]
    strong = [{"stat": {"name": "hp"}, "base_stat": 100}, {"stat": {"name": "attack"}, "base_stat": 100}]

    # Act
    result = battle_compare_stats(weak, strong)

    # Assert
    assert result == -1


def test_battle_compare_stats_draw():
    # Arrange
    stats = [{"stat": {"name": "hp"}, "base_stat": 45}, {"stat": {"name": "attack"}, "base_stat": 49}]

    # Act
    result = battle_compare_stats(stats, stats)

    # Assert
    assert result == 0


battle_compare_stats_cases = [
    (
        [{"stat": {"name": "hp"}, "base_stat": 80}, {"stat": {"name": "speed"}, "base_stat": 90}],
        [{"stat": {"name": "hp"}, "base_stat": 40}, {"stat": {"name": "speed"}, "base_stat": 45}],
        1,
    ),
    (
        [{"stat": {"name": "hp"}, "base_stat": 40}, {"stat": {"name": "speed"}, "base_stat": 45}],
        [{"stat": {"name": "hp"}, "base_stat": 80}, {"stat": {"name": "speed"}, "base_stat": 90}],
        -1,
    ),
    (
        [{"stat": {"name": "hp"}, "base_stat": 50}],
        [{"stat": {"name": "hp"}, "base_stat": 50}],
        0,
    ),
]


@pytest.mark.parametrize("first_stats, second_stats, expected", battle_compare_stats_cases)
def test_battle_compare_stats_parametrized(first_stats, second_stats, expected):
    # Act
    result = battle_compare_stats(first_stats, second_stats)

    # Assert
    assert result == expected
