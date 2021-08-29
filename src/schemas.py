from datetime import datetime
from typing import Optional, List, Tuple

from pydantic import BaseModel, Field

from src.config import get_settings
from src.constants import Status


def to_camel(string: str) -> str:
    """Camel-case a given string e.g. camel_case -> camelCase"""
    return "".join(
        word.capitalize() if i else word for i, word in enumerate(string.split("_"))
    )


class CamelModel(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class JWTPayload(CamelModel):
    player_id: int
    game_id: int
    is_master: bool
    exp: Optional[int]


class PlayerCreate(CamelModel):
    name: str


class GameCreate(CamelModel):
    secs_per_round: Optional[int] = Field(default=get_settings().default_secs_per_round)


class NewGamePayload(CamelModel):
    player: PlayerCreate
    game: GameCreate


class NewPlayerPayload(CamelModel):
    player: PlayerCreate


class Player(CamelModel):
    id: int
    name: str
    score: int

    class Config:
        orm_mode = True


class Game(CamelModel):
    id: int
    status: Status
    secs_per_round: int
    join_link: str
    players: List[Player]

    class Config:
        orm_mode = True


class GameRound(CamelModel):
    id: int
    status: Status
    statement: str
    created_at: datetime
    player_for: Player
    player_against: Player
    vote_results: Tuple[int, int]

    class Config:
        orm_mode = True


class GameSession(CamelModel):
    game_id: int
    player_id: int
    is_master: bool

    class Config:
        allow_population_by_field_name = True


class VotePayload(CamelModel):
    verdict: bool


class Candidate(BaseModel):
    player_id: int
    num_rows: int = 0
    num_for: int = 0
    num_against: int = 0
    score: int = 0
