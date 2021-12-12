from uuid import UUID

from src.domain.exceptions import NotEnoughPlayersError, UniquePlayerNameError
from src.domain.models import Game, Debate, Player
from src.domain.ports.repositories import BaseGameRepo, BaseStatementRepo


MINIMUM_PLAYERS = 3


def new_game(game_name: str, game_repo: BaseGameRepo) -> Game:
    game = Game(game_name)
    return game_repo.save(game)


def start_game(game_id: UUID, game_repo: BaseGameRepo) -> Game:
    game = game_repo.get_available(game_id)

    if len(game.players) < MINIMUM_PLAYERS:
        raise NotEnoughPlayersError(f"You need minimum {MINIMUM_PLAYERS} players...")

    game.start()
    return game


def start_debate(
    game_id: UUID, game_repo: BaseGameRepo, statement_repo: BaseStatementRepo
) -> Debate:
    game = game_repo.get_available(game_id)
    new_statement = statement_repo.get_next_statement({d.id for d in game.debates})

    debate = Debate(
        game.players[0],
        game.players[1],
        new_statement,
    )

    game.debates.append(debate)
    return debate


def add_player_to_game(
    game_id: UUID, player_name: str, game_repo: BaseGameRepo
) -> Player:
    game = game_repo.get_available(game_id)

    if player_name in {p.name for p in game.players}:
        raise UniquePlayerNameError(
            f"Already exists a player named {player_name}, please choose another name"
        )

    new_player = Player(player_name)
    game.add_player(new_player)

    return new_player
