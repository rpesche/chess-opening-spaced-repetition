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
import hashlib

import chess.svg
from chess import Board

from lichess.openings import generate_frequent_move, MovesTree
from anki import create_anki_packages


@dataclass
class CardInfo:
    fen: str
    opponnent_san: str
    moves: list[str]

    def hash(self) -> str:
        payload = self.fen + self.opponnent_san
        return hashlib.md5(payload.encode("utf-8")).hexdigest()


def cards_fom_moves_tree(board: Board, moves_tree: MovesTree) -> dict[str, CardInfo]:
    results: dict[str, CardInfo] = {}
    _cards_fom_moves_tree(board, moves_tree, results)
    return results


def _cards_fom_moves_tree(
    board: Board, moves_tree: MovesTree, results: dict[str, CardInfo]
) -> None:
    # generate
    for opponnent_san, moves in moves_tree.items():
        results_key = board.fen() + opponnent_san

        # Sometimes we get to the same board through different sequence of moves
        if results_key in results:
            continue
        results[results_key] = CardInfo(
            fen=board.fen(), opponnent_san=opponnent_san, moves=list(moves.keys())
        )

    for opponnent_san, moves in moves_tree.items():
        for san, further_moves in moves.items():
            board.push_san(opponnent_san)
            board.push_san(san)
            _cards_fom_moves_tree(board, further_moves, results)
            board.pop()
            board.pop()


def gen_learning_decks(fen: str, deep: int, package_filename: str) -> None:
    board = Board(fen)

    moves_tree = generate_frequent_move(board, deep)
    cards = cards_fom_moves_tree(board, moves_tree)
    create_anki_packages(list(cards.values()), package_filename)


def main() -> None:
    starting_fen = "rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1"
    gen_learning_decks(starting_fen, 2, "output.apkg")


if __name__ == "__main__":
    main()


# TODO: must get all the moves that lead to starting board in order to get info from wikibooks
# The book title are formatted using joined move san, so we must having all of them
