"""
Generate openings anki decks

Usage:
  openings generate from <position> (black|white)
  openings generate

Options:
  -h --help     Show this screen.
  <position>    The start position
"""
from dataclasses import dataclass

import chess
import chess.svg
from rich.pretty import pprint

from lichess.openings import generate_frequent_move
from anki import create_anki_packages


@dataclass
class CardInfo:
    fen: str
    opponnent_san: str
    moves: list[str]


def key_from_oponent_move(board, opponnent_san, moves):
    fen = board.fen()

    yield CardInfo(fen=fen, opponnent_san=opponnent_san, moves=list(moves.keys()))

    for san, further_moves in moves.items():
        for further_san, further_moves in further_moves.items():
            board.push_san(opponnent_san)
            board.push_san(san)
            yield from key_from_oponent_move(board, further_san, further_moves)
            board.pop()
            board.pop()


def main():
    starting_fen = "rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1"
    board = chess.Board(starting_fen)

    result = generate_frequent_move(board, 2)
    # pprint(result, expand_all=True)

    res = []
    for further_san, further_moves in result.items():
        plop = key_from_oponent_move(board, further_san, further_moves)
        res.extend(plop)
    create_anki_packages(res)
    # pprint(res, expand_all=True)
    # fen, color = input_chess_board()

    # board = chess.Board(fen)
    # res = chess.svg.board(board)
    # print(res)
    # with open("truc.svg", "w+") as fd:
    # fd.write(res)


if __name__ == "__main__":
    main()


# TODO: must get all the moves that lead to starting board in order to get info from wikibooks
# The book title are formatted using joined move san, so we must having all of them
