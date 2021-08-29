from typing import Tuple, Optional

from sqlalchemy.orm import Session
from starlette import status

from src.config import Settings, get_settings
from src.constants import GAME_SESSION_KEY
from src.db import get_db
from src.models import GameModel, PlayerModel
from src.schemas import (
    Game,
    NewGamePayload,
    GameSession,
    NewPlayerPayload,
    GameRound,
)
from fastapi import Response, Depends, APIRouter, Request, HTTPException

from src.session_token import GameSessionJWT
from src.use_cases import (
    create_game,
    join_game,
    info_from_jwt_payload,
    create_game_round,
)

router = APIRouter()


def info_from_request(
    request: Request,
    settings: Settings = Depends(get_settings),
    db_session: Session = Depends(get_db),
) -> Tuple[GameModel, PlayerModel]:
    jwt_token = request.cookies.get(GAME_SESSION_KEY)

    if not jwt_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    jwt_session = GameSessionJWT(settings)
    jwt_payload = jwt_session.from_token_str(jwt_token)

    return info_from_jwt_payload(db_session, jwt_payload)


@router.get("/")
def root():
    return {"message": "Hello, World!"}


@router.post("/game", response_model=Game, status_code=status.HTTP_201_CREATED)
def create_game_handler(
    payload: NewGamePayload,
    response: Response,
    db_session: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    new_game, player = create_game(
        db_session=db_session,
        player_schema=payload.player,
        game_schema=payload.game,
    )

    jwt_session = GameSessionJWT(settings)
    game_session = GameSession(
        game_id=new_game.id,
        player_id=player.id,
        is_master=player.is_master,
    )

    response.set_cookie(
        key=GAME_SESSION_KEY, value=jwt_session.to_public_token(game_session)
    )

    return new_game


@router.get("/game", response_model=Game)
def get_game_handler(
    session_info: Tuple[GameModel, PlayerModel] = Depends(info_from_request)
):
    game, player = session_info
    return game


@router.post(
    "/game/join/{join_token}", response_model=Game, status_code=status.HTTP_201_CREATED
)
def join_game_handler(
    join_token: str,
    payload: NewPlayerPayload,
    response: Response,
    db_session: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    game, player = join_game(
        db_session=db_session,
        player_schema=payload.player,
        join_token=join_token,
    )

    jwt_session = GameSessionJWT(settings)
    game_session = GameSession(
        game_id=game.id,
        player_id=player.id,
        is_master=player.is_master,
    )

    response.set_cookie(
        key=GAME_SESSION_KEY, value=jwt_session.to_public_token(game_session)
    )

    return game


@router.post(
    "/game/round", response_model=GameRound, status_code=status.HTTP_201_CREATED
)
def start_round_handler(
    db_session: Session = Depends(get_db),
    session_info: Tuple[GameModel, PlayerModel] = Depends(info_from_request),
):
    game, player = session_info
    if not player.is_master:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return create_game_round(db_session, game)


@router.get("/game/round", response_model=Optional[GameRound])
def get_round_handler(
    session_info: Tuple[GameModel, PlayerModel] = Depends(info_from_request),
):
    game, player = session_info
    if game.rounds:
        return game.rounds[-1]
    return None


"""
TODO:
Endpoints:
* POST Create New Game ---
* POST Join Game ---
* POST Start Round ---
* GET Game ---
* GET Round ---
* POST Vote


"""
