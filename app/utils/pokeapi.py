import requests

BASE_URL = "https://pokeapi.co/api/v2"

def get_pokemon_name(api_id):
    """
        Get a pokemon name from the API pokeapi
    """
    return get_pokemon_data(api_id)['name']

def get_pokemon_stats(api_id):
    """
        Get pokemon stats from the API pokeapi
    """
    return get_pokemon_data(api_id)['stats']

def get_pokemon_data(api_id):
    """
        Get data of pokemon name from the API pokeapi
    """
    return requests.get(f"{BASE_URL}/pokemon/{api_id}", timeout=10).json()

def battle_pokemon(first_api_id, second_api_id):
    """
        Do battle between 2 pokemons
    """
    premier_pokemon = get_pokemon_data(first_api_id)
    second_pokemon = get_pokemon_data(second_api_id)
    battle_result = 0
    if battle_result > 0:
        return premier_pokemon
    if battle_result < 0:
        return second_pokemon
    return {'winner': 'draw'}

def battle_compare_stats(first_pokemon_stats, second_pokemon_stats):
    first_stats = {stat['stat']['name']: stat['base_stat'] for stat in first_pokemon_stats}
    second_stats = {stat['stat']['name']: stat['base_stat'] for stat in second_pokemon_stats}

    score = 0
    for stat_name, first_value in first_stats.items():
        second_value = second_stats.get(stat_name)
        if second_value is None:
            continue
        if first_value > second_value:
            score += 1
        elif first_value < second_value:
            score -= 1

    if score > 0:
        return 1
    if score < 0:
        return -1
    return 0