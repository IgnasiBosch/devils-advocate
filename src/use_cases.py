import operator
import random
from typing import Tuple, List

from sqlalchemy.orm import Session

from src.constants import Status
from src.db import transaction, not_found_converter
from src.models import GameModel, PlayerModel, RoundModel, VoteModel
from src.schemas import PlayerCreate, GameCreate, JWTPayload, Candidate


def create_game(
    db_session: Session, game_schema: GameCreate, player_schema: PlayerCreate
) -> Tuple[GameModel, PlayerModel]:
    with transaction(db_session):
        new_game = GameModel(**game_schema.dict())
        db_session.add(new_game)
        db_session.flush()

        player = PlayerModel(
            **player_schema.dict(), game_id=new_game.id, is_master=True
        )
        db_session.add(player)

    return new_game, player


@not_found_converter
def join_game(
    db_session: Session, join_token: str, player_schema: PlayerCreate
) -> Tuple[GameModel, PlayerModel]:
    with transaction(db_session):
        game = db_session.query(GameModel).filter_by(join_token=join_token).one()

        player = PlayerModel(**player_schema.dict(), game_id=game.id)
        db_session.add(player)

    return game, player


@not_found_converter
def info_from_jwt_payload(
    db_session: Session, jwt_payload: JWTPayload
) -> Tuple[GameModel, PlayerModel]:
    game = db_session.query(GameModel).filter_by(id=jwt_payload.game_id).one()

    player = (
        db_session.query(PlayerModel)
        .filter_by(id=jwt_payload.player_id, game_id=jwt_payload.game_id)
        .one()
    )

    return game, player


topics = {
    "Abortion",
    "Capitalism",
    "Religion",
    "Marriage",
    "Feminism",
    "Vaccination",
    "Euthanasia",
    "Porn",
    "Prostitution",
    "Guns",
    "Free Speech",
    "Government",
    "Death Penalty",
}

statements = {
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
}
"""
https://blog.prepscholar.com/good-debate-topics
https://games4esl.com/controversial-debate-topics/
"""


def create_game_round(db_session: Session, game: GameModel) -> RoundModel:

    if len(game.players) < 3:
        raise ValueError("Not enough players. Minimum 3")
    if game.rounds and game.rounds[-1].status == Status.PLAYING:
        raise ValueError("A round is still in play")

    player_for_id, player_against_id = select_participants(round_candidates(game))
    statement = random.choice(
        [t for t in statements if t not in {i.statement for i in game.rounds}]
    )

    game_round = RoundModel(
        statement=statement,
        player_for_id=player_for_id,
        player_against_id=player_against_id,
        game_id=game.id,
    )

    db_session.add(game_round)
    db_session.commit()

    return game_round


def round_candidates(game: GameModel) -> List[Candidate]:
    player_stats = {
        i.id: Candidate(player_id=i.id, score=i.score) for i in game.players
    }
    for game_round in game.rounds:
        player_stats[game_round.player_for.id].num_rows += 1
        player_stats[game_round.player_for.id].num_for += 1
        player_stats[game_round.player_against.id].num_rows += 1
        player_stats[game_round.player_against.id].num_against += 1

    return list(player_stats.values())


def select_participants(candidates: List[Candidate]) -> Tuple[int, int]:
    sorted_by_participation = sorted(candidates, key=operator.attrgetter("num_rows"))
    sorted_by_position = sorted(
        sorted_by_participation[:2], key=operator.attrgetter("num_for")
    )
    return sorted_by_position[0].player_id, sorted_by_position[1].player_id


def add_vote_to_round(
    db_session: Session, game_round: RoundModel, player: PlayerModel, verdict: bool
) -> RoundModel:

    if player in game_round.participants:
        raise ValueError("Participants can't vote")
    if player in {i.player for i in game_round.votes}:
        raise ValueError("You already voted")

    with transaction(db_session):
        vote = VoteModel(verdict=verdict, player=player, round=game_round)
        db_session.add(vote)
        db_session.flush()

        if (len(game_round.votes) + 1) >= (len(game_round.game.players) - 2):
            game_round.status = Status.FINISHED

            total_true_votes, total_false_votes = game_round.vote_results
            if total_true_votes != total_false_votes:
                verdict = total_true_votes > total_false_votes
                game_round.verdict = verdict
                if verdict is True:
                    game_round.player_for.score += 1
                else:
                    game_round.player_against.score +=1

    return game_round
