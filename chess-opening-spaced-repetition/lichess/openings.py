from berserk import Client
from typing import TypedDict


class Move(TypedDict):
    san: str
    play_rate: float
    # win_rate: float
    # loose_rate: float
    # draw_rate: float


def get_frequent_moves_from_fen(fen: str, database: str = "lichess"):
    client = Client()
    openings_info = client.opening_explorer.get_lichess_games(position=fen)
    moves = openings_info["moves"]
    total_games = sum([move["white"] + move["black"] + move["draws"] for move in moves])

    for move in moves:
        play_rate = (move["white"] + move["black"] + move["draws"]) / total_games * 100.0
        yield {
            "san": move["san"],
            "play_rate": play_rate
        }

def _generate_frequent_move(board, results, iteration=0):
    if iteration <= 0:
        return

    percent = 10.0

    moves = list(get_frequent_moves_from_fen(board.fen()))
    selected_opponent_moves = [move for move in moves if move["play_rate"] > percent]

    for opponent_move in selected_opponent_moves:
        san = opponent_move["san"]
        results[san] = {}

        board.push_san(san)
        opening_moves = list(get_frequent_moves_from_fen(board.fen()))
        for opening_move in opening_moves:
            if opening_move["play_rate"] < percent:
                continue
            results[san][opening_move["san"]] = {}
            board.push_san(opening_move["san"])
            _generate_frequent_move(board, results[san][opening_move["san"]], iteration - 1)
            board.pop()
        board.pop()


def generate_frequent_move(board, iteration=0):
    results = {}
    _generate_frequent_move(board, results, iteration)
    return results
