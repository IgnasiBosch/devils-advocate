import time

import typer
from click import Choice

from src.adapters.repositories import (
    populate_statements,
    get_game_repo,
    get_statement_repo,
)
from src.application.use_cases import (
    start_game,
    add_player_to_game,
    start_debate,
    new_game,
)
from src.domain.constants import DebateSide
from src.domain.exceptions import NotEnoughPlayersError, UniquePlayerNameError

ROUND_TIME_SECS = 30
WAIT_TIME_SECS = 5

game_repo = get_game_repo()
statement_repo = get_statement_repo()


def add_players_handler(game):
    player_name = typer.prompt(
        "Add a player (leave it blank to continue)", default="", show_default=False
    )
    if not player_name:
        try:
            start_game(game.id, game_repo)
        except NotEnoughPlayersError as exc:
            typer.echo(str(exc))
            return add_players_handler(game)
        else:
            return game

    try:
        add_player_to_game(game.id, player_name, game_repo)
    except UniquePlayerNameError as exc:
        typer.echo(str(exc))
        return add_players_handler(game)
    else:
        add_players_handler(game)


def start_debate_handler(game):
    debate = start_debate(game.id, game_repo, statement_repo)

    typer.echo("")
    typer.echo(f"Statement: {debate.statement.assertion}")
    time.sleep(WAIT_TIME_SECS * 2)

    typer.echo("")
    typer.echo(f"Agree: {debate.agree.name}")
    time.sleep(WAIT_TIME_SECS)

    with typer.progressbar(range(ROUND_TIME_SECS)) as progress:
        for _ in progress:
            time.sleep(1)

    typer.echo("")
    typer.echo(f"Disagree: {debate.disagree.name}")
    time.sleep(WAIT_TIME_SECS)

    with typer.progressbar(range(ROUND_TIME_SECS)) as progress:
        for _ in progress:
            time.sleep(1)


def voting_handler(game):
    votes = {"0": DebateSide.DISAGREE, "1": DebateSide.AGREE}
    debate = game.get_current_debate()

    for player in game.players:
        if player not in debate.participants():
            vote_val = typer.prompt(
                f"{player.name} emit your vote [0: Disagree, 1: Agree]",
                type=Choice(["0", "1"]),
                hide_input=True,
                show_choices=False,
            )
            vote = votes[vote_val]
            debate.vote(player, vote)

    typer.echo("")
    typer.echo("All votes were emitted")

    time.sleep(WAIT_TIME_SECS)
    verdict = debate.get_verdict()
    typer.echo(f"Verdict was: {verdict}")
    time.sleep(WAIT_TIME_SECS)

    typer.echo("")
    for player, score in sorted(
        game.get_score().items(), key=lambda item: item[1], reverse=True
    ):
        typer.echo(f"{player.name}: {score}")

    typer.echo("--------------")
    typer.echo("")


def main():
    populate_statements()
    typer.echo("")
    typer.echo("Welcome to Devil's Advocate!!")
    typer.echo("-----------------------------")

    typer.echo("")
    game_name = typer.prompt("Chose a name for your game")
    game = new_game(game_name, game_repo)
    add_players_handler(game)

    typer.echo("")
    typer.prompt(
        "Press enter when you are ready to start",
        prompt_suffix="...",
        default="",
        show_default=False,
    )

    while True:
        start_debate_handler(game)

        typer.echo("")
        voting_handler(game)

        typer.echo("")
        action = typer.prompt(
            "Press enter when you are ready to start next debate (or Q to quit)",
            default="",
            prompt_suffix="",
            show_default=False,
        )
        if action.lower() == "q":
            break

    typer.echo("")
    for player, score in sorted(
        game.get_score().items(), key=lambda item: item[1], reverse=True
    ):
        typer.echo(f"{player.name}: {score}")

    typer.echo("--------------")
    typer.echo("")


if __name__ == "__main__":
    typer.run(main)
