from enum import Enum

GAME_SESSION_KEY = "GAMESESSION"


class Status(str, Enum):
    PENDING = "pending"
    PLAYING = "playing"
    FINISHED = "finished"
