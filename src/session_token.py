from __future__ import annotations
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi.encoders import jsonable_encoder
from jose import ExpiredSignatureError, JWTError, jwt

from src.config import Settings
from src.schemas import GameSession, JWTPayload


class ExpiredSession(Exception):
    ...


class SessionError(ValueError):
    ...


class GameSessionJWT:
    def __init__(self, settings: Settings):
        self.secret_key = settings.session_token_key
        self.algorithm = settings.session_token_algorithm
        self.minutes_to_exp = settings.session_token_exp_time

    def to_public_token(self, game_session: GameSession):
        jwt_token = JWTPayload(
            player_id=game_session.player_id,
            game_id=game_session.game_id,
            is_master=game_session.is_master,
        )
        return self.to_jwt(jwt_token)

    def from_token_str(self, jwt_token: str) -> JWTPayload:
        return self.decode(jwt_token)

    def encode(self, payload: dict) -> str:
        return jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm,
        )

    def decode(self, token_str: str, verify_exp=True) -> JWTPayload:
        try:
            payload = jwt.decode(
                token_str,
                self.secret_key,
                algorithms=[self.algorithm],
                options={"verify_exp": verify_exp},
            )
            return JWTPayload(**payload)
        except ExpiredSignatureError:
            raise ExpiredSession
        except JWTError:
            raise SessionError

    def to_jwt(
        self, jwt_payload: JWTPayload, expires_delta: Optional[timedelta] = None
    ) -> str:
        expires_delta = expires_delta or timedelta(self.minutes_to_exp)

        # https://docs.python.org/3.8/library/datetime.html#datetime.datetime.utcnow
        expire = datetime.now(timezone.utc) + expires_delta

        jwt_payload.exp = int(datetime.timestamp(expire))
        encoded_token = self.encode(
            jsonable_encoder(jwt_payload.dict(exclude_none=True, by_alias=True))
        )
        return encoded_token
