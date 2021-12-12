from enum import Enum


class GameStatus(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    FINISHED = "FINISHED"


class DebateSide(str, Enum):
    AGREE = "agree"
    DISAGREE = "disagree"


class Verdict(str, Enum):
    AGREE = "agree"
    DISAGREE = "disagree"
    DRAW = "draw"
