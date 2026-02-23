# TEST EXAM — GROUPE 2 (4 membres)

**API RESTful de gestion de dresseurs Pokémon, de leurs Pokémon et de leur inventaire.**

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Status](https://img.shields.io/badge/Status-Exam%20Project-blueviolet?style=for-the-badge)

---

## Table des matières

- [Groupe](#groupe)
- [Description](#description)
- [Réalisations](#réalisations)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Endpoints API](#endpoints-api)
- [Tests unitaires](#tests-unitaires)
- [Tests de performance — Locust](#tests-de-performance--locust)
- [Qualité du code — Pylint](#qualité-du-code--pylint)
- [Auteurs](#auteurs)

---

## Groupe

**Groupe 2 — 4 membres**  
Dépôt GitHub : [https://github.com/4GUYS-MSPR/test_exam](https://github.com/4GUYS-MSPR/test_exam)

- Théo DANEL
- Danaël LEGRAND
- Sebastien LOTTEN
- Mael BOYAVAL 

---

## Description

**PokéManager API** est un service backend RESTful construit avec **FastAPI** et **SQLAlchemy**, développé dans le cadre d'un projet d'examen EPSI.  
Il permet de gérer des dresseurs Pokémon, de leur assigner des Pokémon (données récupérées en temps réel depuis [PokéAPI](https://pokeapi.co/)), de tenir un inventaire d'objets, et de faire combattre des Pokémon entre eux.

Le projet inclut :
- Une base de données **SQLite** gérée via l'ORM SQLAlchemy
- Intégration avec l'API externe **PokéAPI** (`https://pokeapi.co/api/v2`)
- Documentation interactive auto-générée via **Swagger UI** et **ReDoc**
- Suite de tests complète avec **pytest**, **coverage** et **locust** pour les tests de charge

---

## Réalisations

### Endpoint de combat entre 2 Pokémon

Ajout d'un endpoint `GET /pokemons/fight` permettant de faire combattre 2 Pokémon en fournissant leurs IDs en base de données.

**Logique de combat :**

- Les statistiques des 2 Pokémon sont récupérées depuis la PokéAPI (`hp`, `attack`, `defense`, `special-attack`, `special-defense`, `speed`).
- Chaque stat est comparée 1 par 1 (health vs health, attack vs attack, etc.).
- Le Pokémon ayant le plus grand nombre de stats supérieures gagne.
- En cas d'égalité parfaite, le résultat est un match nul (`draw: true`).

**Exemple de requête :**
```
GET /pokemons/fight?first_pokemon_id=1&second_pokemon_id=2
```

**Exemple de réponse :**
```json
{
  "winner": "pikachu",
  "draw": false
}
```

---

### Endpoint — 3 Pokémon aléatoires *(Groupe de 4)*

Ajout d'un endpoint `GET /pokemons/random` listant 3 Pokémon aléatoires depuis la PokéAPI, avec affichage de leurs statistiques complètes (`hp`, `attack`, `defense`, `special-attack`, `special-defense`, `speed`).

---

## Installation

### Prérequis

- Python **3.10** ou supérieur
- `pip` et `venv`

### Étapes

1. **Cloner le dépôt**

   ```bash
   git clone https://github.com/4GUYS-MSPR/test_exam.git
   cd test_exam
   ```

2. **Créer et activer un environnement virtuel**

   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # macOS / Linux
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Installer les dépendances**

   ```bash
   pip install -r requirements.txt
   ```

4. **Lancer le serveur de développement**

   ```bash
   uvicorn main:app --reload
   ```

   L'API est disponible à l'adresse `http://127.0.0.1:8000`.

---

## Utilisation

Une fois le serveur lancé, ouvrir dans le navigateur :

- **`http://127.0.0.1:8000/docs`** — Swagger UI (interactif)
- **`http://127.0.0.1:8000/redoc`** — Documentation ReDoc

**Exemple — créer un dresseur :**
```bash
curl -X POST "http://127.0.0.1:8000/trainers/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Ash Ketchum", "birthdate": "1997-04-01"}'
```

---

## Endpoints API

### Dresseurs — `/trainers`

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `POST` | `/trainers/` | Créer un dresseur |
| `GET` | `/trainers` | Lister tous les dresseurs |
| `GET` | `/trainers/{trainer_id}` | Obtenir un dresseur par ID |
| `POST` | `/trainers/{trainer_id}/pokemon/` | Assigner un Pokémon à un dresseur |
| `POST` | `/trainers/{trainer_id}/item/` | Ajouter un objet à l'inventaire |

### Pokémon — `/pokemons`

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/pokemons/` | Lister tous les Pokémon |
| `GET` | `/pokemons/fight` | Faire combattre 2 Pokémon (par ID) |
| `GET` | `/pokemons/random` | Obtenir 3 Pokémon aléatoires avec leurs stats |

### Objets — `/items`

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/items/` | Lister tous les objets |

---

## Tests unitaires

### Lancer les tests

```bash
pytest --cov=app
```

### Lancer les tests avec rapport de couverture HTML

```bash
pytest --cov=app --cov-report=html
```

### Structure des tests

| Fichier | Type | Description |
|---------|------|-------------|
| `test/routers/trainers_test.py` | Unitaires + Mocks | Tests sur les endpoints des dresseurs |
| `test/routers/pokemons_test.py` | Unitaires + Mocks | Tests sur les endpoints des Pokémon |
| `test/routers/items_test.py` | Unitaires | Tests sur les endpoints des objets |
| `test/utils/pokeapi_test.py` | Unitaires + Mocks | Tests sur l'intégration PokéAPI |
| `test/utils/utils_test.py` | Unitaires | Tests sur les utilitaires |

**Objectifs groupe de 4 :**
- ✅ 7 tests unitaires minimum
- ✅ 5 tests unitaires avec mocks minimum
- ✅ Couverture de code > 85 %

---

## Tests de performance — Locust

Les tests de charge sont définis dans `locustfile.py` et configurés via `.locust.conf`.

### Configuration (`.locust.conf`)

| Paramètre | Valeur |
|-----------|--------|
| `host` | `http://127.0.0.1:8000/` |
| `users` | 1000 |
| `spawn-rate` | 1 utilisateur/seconde |
| `run-time` | 1 minute |
| `headless` | true |
| `html` | true (rapport généré automatiquement) |
| `csv` | `res/res.csv` (historique complet) |

### Lancer les tests Locust

```bash
locust
```

---

## Qualité du code — Pylint

Objectif groupe de 4 : **note ≥ 8.5 / 10**

```bash
pylint app/
```