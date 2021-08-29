import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.config import Settings, get_settings
from src.constants import GAME_SESSION_KEY
from src.db import get_engine, Base
from src.main import app as orig_get_app
from src.schemas import Candidate
from src.use_cases import select_participants


def get_settings_override():
    return Settings(database_uri="sqlite:///test_database.db")


@pytest.fixture(scope="session")
def app() -> FastAPI:
    testing_app = orig_get_app
    # testing_app.dependency_overrides[get_db] = override_get_db
    testing_app.dependency_overrides[get_settings] = get_settings_override
    Base.metadata.create_all(get_engine())

    yield testing_app

    Base.metadata.drop_all(get_engine())


@pytest.fixture(scope="session")
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


def test_create_game(client):
    payload = {"player": {"name": "Kevin"}, "game": {"secsPerRound": 30}}
    response_1 = client.post("/game", json=payload)
    assert response_1.status_code == 201
    game = response_1.json()
    assert len(game["players"]) == 1

    payload = {"player": {"name": "Mary Ann"}}
    response_2 = client.post(game.get("joinLink"), json=payload)
    assert response_2.status_code == 201
    game = response_2.json()
    assert len(game["players"]) == 2

    response_3 = client.post(
        "/game/round",
        cookies={GAME_SESSION_KEY: response_1.cookies.get(GAME_SESSION_KEY)},
    )
    assert response_3.status_code == 201
    game_round_1 = response_3.json()

    response_4 = client.post(
        "/game/round",
        cookies={GAME_SESSION_KEY: response_1.cookies.get(GAME_SESSION_KEY)},
    )
    assert response_4.status_code == 201
    game_round_2 = response_4.json()


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
