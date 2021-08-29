from __future__ import annotations

import secrets
from datetime import datetime
from enum import Enum
from typing import Optional, Any, List

from sqlalchemy import (
    Column,
    Integer,
    String,
    TypeDecorator,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    Boolean,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import relationship

from src.constants import Status
from src.db import Base


def generate_join_token() -> str:
    return secrets.token_urlsafe(10)


class AsEnum(TypeDecorator):
    impl = String(50)

    def __init__(self, enumtype, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._enumtype = enumtype

    def process_bind_param(self, value: Optional[Any], dialect):
        if value is None:
            return None
        if isinstance(value, str):
            return value
        if isinstance(value, Enum):
            return value.value  # noqa

    def process_result_value(self, value, dialect):
        return value and self._enumtype(value)


class GameModel(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(AsEnum(Status), default=Status.PENDING, nullable=False)
    secs_per_round = Column(Integer, nullable=False)
    join_token = Column(
        String(50), nullable=False, default=generate_join_token, unique=True
    )

    players: List[PlayerModel] = relationship(
        "PlayerModel", order_by="PlayerModel.created_at", cascade="all, delete-orphan"
    )  # type:ignore

    rounds: List[RoundModel] = relationship(
        "RoundModel", order_by="RoundModel.created_at", cascade="all, delete-orphan"
    )  # type:ignore

    @property
    def join_link(self):
        return f"/game/join/{self.join_token}"


class PlayerModel(Base):
    __tablename__ = "players"
    __table_args__ = (
        UniqueConstraint(
            "name",
            "game_id",
            name="idx_uniq_part_name_per_game",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    name = Column(String(100), nullable=False)
    score = Column(Integer, default=0)
    is_master = Column(Boolean, default=False)
    game_id = Column(
        Integer,
        ForeignKey(
            "games.id",
            ondelete="CASCADE",
            name="player_game_id_fkey",
        ),
        nullable=False,
    )  # type:ignore


class RoundModel(Base):
    __tablename__ = "rounds"

    id = Column(Integer, primary_key=True, index=True)
    statement = Column(String(500), nullable=False)
    verdict = Column(Boolean, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(AsEnum(Status), default=Status.PLAYING, nullable=False)
    player_for_id = Column(ForeignKey("players.id"), nullable=False)
    player_against_id = Column(ForeignKey("players.id"), nullable=False)
    game_id = Column(
        Integer,
        ForeignKey(
            "games.id",
            ondelete="CASCADE",
            name="round_game_id_fkey",
        ),
        nullable=False,
    )  # type:ignore

    player_for: PlayerModel = relationship(
        "PlayerModel", primaryjoin="RoundModel.player_for_id==PlayerModel.id"
    )
    player_against: PlayerModel = relationship(
        "PlayerModel", primaryjoin="RoundModel.player_against_id==PlayerModel.id"
    )
