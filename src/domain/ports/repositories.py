from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.models import Game, Statement


class BaseGameRepo(ABC):
    @abstractmethod
    def get(self, game_id: UUID) -> Game:
        ...

    @abstractmethod
    def get_available(self, game_id: UUID) -> Game:
        ...

    @abstractmethod
    def save(self, game: Game) -> Game:
        ...


class BaseStatementRepo(ABC):
    @abstractmethod
    def get(self, statement_id: UUID) -> Statement:
        ...

    @abstractmethod
    def get_next_statement(self, debated_statement_ids: set[UUID]) -> Statement:
        ...

    @abstractmethod
    def save(self, statement: Statement) -> Statement:
        ...
