from __future__ import annotations

from collections import Counter
from uuid import UUID, uuid4
from dataclasses import dataclass, field
from typing import Optional

from .constants import GameStatus, DebateSide, Verdict


class Game:
    def __init__(self, name: str):
        self.id: UUID = uuid4()
        self.name: str = name
        self.players: list[Player] = []
        self.game_master: Optional[Player] = None
        self.status: GameStatus = GameStatus.PENDING
        self.debates: list[Debate] = []

    def add_player(self, player: Player):
        if player.name in {p.name for p in self.players}:
            raise ValueError(f"Player named {player.name} already exists!")

        self.players.append(player)

        if len(self.players) == 1:
            self.game_master = player

    def start(self):
        if self.status is not GameStatus.PENDING:
            raise ValueError(
                f"Game {self.name} can't be started. Current status: {self.status}"
            )

        self.status = GameStatus.RUNNING

    def get_current_debate(self) -> Debate:
        try:
            return self.debates[-1]
        except KeyError:
            raise ValueError("You need to start a debate first")

    def get_score(self) -> dict[Player, float]:
        score: dict[Player, float] = {}
        for player in self.players:
            score[player] = 0
        for debate in self.debates:
            if debate.get_verdict() is Verdict.AGREE:
                score[debate.agree] += 1
            if debate.get_verdict() is Verdict.DISAGREE:
                score[debate.disagree] += 1
            if debate.get_verdict() is Verdict.DRAW:
                score[debate.agree] += 0.5
                score[debate.disagree] += 0.5

        return score

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.name}")'


@dataclass(frozen=True)
class Player:
    name: str
    id: UUID = field(default_factory=uuid4)

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.name}")'


class Debate:
    def __init__(self, agree: Player, disagree: Player, statement: Statement):
        self.id: UUID = uuid4()
        self.agree: Player = agree
        self.disagree: Player = disagree
        self.statement: Statement = statement
        self.votes: dict[Player, DebateSide] = {}

    def vote(self, player: Player, side: DebateSide):
        self.votes[player] = side

    def participants(self) -> set[Player]:
        return {self.agree, self.disagree}

    def get_verdict(self) -> Verdict:
        votes = [v for v in self.votes.values()]
        if not votes:
            raise ValueError("No votes emitted")

        c = Counter(votes)
        result = c.most_common(2)
        if len(result) == 1:
            return Verdict(result[0][0].value)
        if result[0][1] != result[1][1]:
            return Verdict(result[0][0].value)

        return Verdict.DRAW


@dataclass(frozen=True)
class Statement:
    assertion: str
    id: UUID = field(default_factory=uuid4)
    language: str = "en"

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.assertion}")'
