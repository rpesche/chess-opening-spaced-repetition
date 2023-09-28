from chess import Board
import vcr

from lichess.openings import generate_frequent_move
from openings import cards_fom_moves_tree


@vcr.use_cassette(
    "fixtures/vcr_cassettes/french_defense_deep_2.yaml", record_mode="none"
)
def test_generating_move_from_board():
    # French defense board
    starting_fen = "rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1"
    board = Board(starting_fen)
    deep = 2
    moves_tree = generate_frequent_move(board, deep)
    cards = cards_fom_moves_tree(board, moves_tree)
    assert len(cards) == 7
