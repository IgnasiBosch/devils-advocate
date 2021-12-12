import random
from functools import lru_cache
from uuid import UUID

from src.domain.constants import GameStatus
from src.domain.exceptions import GameError
from src.domain.models import Game, Statement
from src.domain.ports.repositories import BaseGameRepo, BaseStatementRepo


class MemoryGameRepo(BaseGameRepo):
    def __init__(self):
        self.games: dict[UUID, Game] = {}

    def get(self, game_id: UUID) -> Game:
        return self.games.get(game_id)

    def get_available(self, game_id: UUID) -> Game:
        game = self.games.get(game_id)
        if game is None:
            raise GameError("This game doesn't exist")
        if game.status is GameStatus.FINISHED:
            raise GameError("This game already finished!")

        return game

    def save(self, game: Game) -> Game:
        self.games[game.id] = game
        return game


@lru_cache
def get_game_repo() -> BaseGameRepo:
    return MemoryGameRepo()


class MemoryStatementRepo(BaseStatementRepo):
    def __init__(self):
        self.statements: dict[UUID, Statement] = {}

    def get(self, statement_id) -> Statement:
        return self.statements.get(statement_id)

    def get_next_statement(self, debated_statement_ids: set[UUID]) -> Statement:
        pending_statements = set(self.statements.keys()).difference(
            debated_statement_ids
        )

        if not pending_statements:
            raise ValueError("You completed all statements!")

        return self.statements[random.choice(list(pending_statements))]

    def save(self, statement: Statement) -> Statement:
        self.statements[statement.id] = statement
        return statement


@lru_cache
def get_statement_repo() -> BaseStatementRepo:
    return MemoryStatementRepo()


def populate_statements():
    statements = [
        "Testing on animals should be banned",
        "The death penalty is sometimes justified",
        "Women should be paid less than men in some professions",
        "Assisted suicide should be made legal",
        "The voting age should be reduced to 16",
        "Smoking should be made illegal everywhere",
        "Prisoners should be allowed to vote",
        "Drug addicts should get help not punishment",
        "Advertising to children should be banned",
        "Beauty competitions create unrealistic beauty standards",
        "Police should be immune from prosecution",
        "Violent video games should be banned",
        "Obese people should pay more for healthcare",
        "Healthcare should be free for everyone",
        "Rich people should pay more taxes",
        "War is never justified",
        "Some soft drugs should be made legal",
        "Marriage is no longer necessary",
        "Children should not have smart phones",
        "If you have more money you will be happier",
        "Governments shouldn’t track its citizens",
        "People should have to take a test to become a parent",
        "Fast food should be banned",
        "Men and women should be allowed to compete against each other in the Olympics",
        "Celebrities should earn less money",
        "All people should receive a basic income",
        "Everyone has the right to own a gun",
        "The age you can buy alcohol should be increased to 25",
        "Eating meat is unethical",
        "Social media has ruined society",
    ]

    statement_repo = get_statement_repo()

    for statement in statements:
        statement_repo.save(Statement(statement))
