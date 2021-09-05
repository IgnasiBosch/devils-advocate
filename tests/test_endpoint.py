import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.constants import GAME_SESSION_KEY
from src.db import Base, get_engine
from src.main import app as orig_get_app
from src.schemas import Candidate
from src.use_cases import select_participants


@pytest.fixture(scope="session")
def app() -> FastAPI:
    testing_app = orig_get_app
    yield testing_app


@pytest.fixture(scope="session")
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture
def clear_all():
    yield
    Base.metadata.drop_all(get_engine())


def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200


def test_full_game_scenario(client, clear_all):

    # Creating a Game
    payload = {"player": {"name": "Kevin Lomax"}, "game": {"secsPerRound": 30}}
    response_1 = client.post("/game", json=payload)
    assert response_1.status_code == 201
    game = response_1.json()
    assert len(game["players"]) == 1

    # Joining a Game
    payload = {"player": {"name": "Mary Ann Lomax"}}
    response_2 = client.post(game.get("joinLink"), json=payload)
    assert response_2.status_code == 201
    game = response_2.json()
    assert len(game["players"]) == 2

    # Can't start until at least 3 players
    response_3 = client.post(
        "/game/rounds",
        cookies={GAME_SESSION_KEY: response_1.cookies.get(GAME_SESSION_KEY)},
    )
    assert response_3.status_code == 422

    # Joining a Game
    payload = {"player": {"name": "John Milton"}}
    response_4 = client.post(game.get("joinLink"), json=payload)
    assert response_4.status_code == 201
    game = response_4.json()
    assert len(game["players"]) == 3

    # Joining a Game
    payload = {"player": {"name": "Alexander Cullen"}}
    response_5 = client.post(game.get("joinLink"), json=payload)
    assert response_5.status_code == 201
    game = response_5.json()
    assert len(game["players"]) == 4

    # Only the master of the game can start it
    response_6 = client.post(
        "/game/rounds",
        cookies={GAME_SESSION_KEY: response_2.cookies.get(GAME_SESSION_KEY)},
    )
    assert response_6.status_code == 401

    # Start round
    response_7 = client.post(
        "/game/rounds",
        cookies={GAME_SESSION_KEY: response_1.cookies.get(GAME_SESSION_KEY)},
    )
    assert response_7.status_code == 201
    game_round_1 = response_7.json()
    assert game_round_1["numVotes"] == 0
    assert game_round_1["verdict"] is None

    # A Participant can't vote
    payload = {"verdict": False}
    response_8 = client.post(
        "/game/round/vote",
        json=payload,
        cookies={GAME_SESSION_KEY: response_2.cookies.get(GAME_SESSION_KEY)},
    )
    assert response_8.status_code == 422

    # Voting for a verdict
    payload = {"verdict": True}
    response_9 = client.post(
        "/game/round/vote",
        json=payload,
        cookies={GAME_SESSION_KEY: response_4.cookies.get(GAME_SESSION_KEY)},
    )
    assert response_9.status_code == 201
    game_round_1 = response_9.json()
    assert game_round_1["numVotes"] == 1
    assert game_round_1["verdict"] is None

    # Can't vote twice
    payload = {"verdict": True}
    response_10 = client.post(
        "/game/round/vote",
        json=payload,
        cookies={GAME_SESSION_KEY: response_4.cookies.get(GAME_SESSION_KEY)},
    )
    assert response_10.status_code == 422

    # Voting for a verdict
    payload = {"verdict": True}
    response_11 = client.post(
        "/game/round/vote",
        json=payload,
        cookies={GAME_SESSION_KEY: response_5.cookies.get(GAME_SESSION_KEY)},
    )
    assert response_11.status_code == 201
    game_round_1 = response_11.json()

    assert game_round_1["numVotes"] == 2
    assert game_round_1["verdict"] is True
    assert game_round_1["status"] == "finished"

    response_12 = client.get(
        "/game",
        cookies={GAME_SESSION_KEY: response_5.cookies.get(GAME_SESSION_KEY)},
    )
    assert response_12.status_code == 200
    game = response_12.json()

    assert game["players"] == [
        {"id": 1, "name": "Kevin Lomax", "score": 1},
        {"id": 2, "name": "Mary Ann Lomax", "score": 0},
        {"id": 3, "name": "John Milton", "score": 0},
        {"id": 4, "name": "Alexander Cullen", "score": 0},
    ]


@pytest.mark.parametrize(
    "candidates, expected",
    (
        (
            [
                Candidate(player_id=1, num_rows=0, num_for=0, num_against=0, score=0),
                Candidate(player_id=2, num_rows=2, num_for=0, num_against=0, score=0),
                Candidate(player_id=3, num_rows=1, num_for=0, num_against=0, score=0),
            ],
            (1, 3),
        ),
        (
            [
                Candidate(player_id=1, num_rows=0, num_for=1, num_against=0, score=0),
                Candidate(player_id=2, num_rows=2, num_for=0, num_against=0, score=0),
                Candidate(player_id=3, num_rows=1, num_for=0, num_against=0, score=0),
            ],
            (3, 1),
        ),
    ),
)
def test_select_participants(candidates, expected):
    result = select_participants(candidates)
    assert result == expected
