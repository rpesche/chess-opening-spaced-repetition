from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING
from pathlib import Path

import chess.svg
import chess

if TYPE_CHECKING:
    from openings import CardInfo
import genanki


def create_svg_board(
    fen: str, opponnent_san: str | None = None, moves: list[str] = []
) -> chess.svg.SvgWrapper:
    board = chess.Board(fen)
    last_move_to_display = None
    next_moves_to_display = []

    board.push_san(opponnent_san)
    last_move_to_display = board.move_stack[-1]

    for move in moves:
        board.push_san(move)
        last_move = board.move_stack[-1]
        board.pop()
        next_moves_to_display.append(
            chess.svg.Arrow(last_move.from_square, last_move.to_square)
        )

    svg_file = chess.svg.board(
        board,
        lastmove=last_move_to_display,
        arrows=next_moves_to_display,
        orientation=chess.BLACK,
    )
    return svg_file


def create_anki_packages(cards: list["CardInfo"], package_filename: str):
    # TODO compute id base on generation parameters
    # TODO make title more explicite (wikibooks ?)
    my_deck = genanki.Deck(2059400110, "my decks")
    my_model = genanki.Model(
        1607392319,
        "Opening move",
        fields=[
            {"name": "recto"},
            {"name": "verso"},
        ],
        templates=[
            {"name": "Move 1", "qfmt": "{{recto}}", "afmt": "{{verso}}"},
        ],
    )

    file_directory = TemporaryDirectory()
    package_files = []
    for card in cards:
        card_name = card.hash()

        recto_svg = create_svg_board(card.fen, opponnent_san=card.opponnent_san)
        recto_file_name = f"{card_name}_recto.svg"
        recto_file = file_directory.name / Path(recto_file_name)
        with open(recto_file, "w+") as fd:
            fd.write(recto_svg)

        verso_svg = create_svg_board(
            card.fen, opponnent_san=card.opponnent_san, moves=card.moves
        )
        verso_file_name = f"{card_name}_verso.svg"
        verso_file = file_directory.name / Path(verso_file_name)
        with open(verso_file, "w+") as fd:
            fd.write(verso_svg)

        my_note = genanki.Note(
            model=my_model,
            fields=[
                f'<img style="display: block;margin: 0 auto;" src="{recto_file_name}">',
                f'<img style="display: block;margin: 0 auto;" src="{verso_file_name}">',
            ],
        )

        package_files.extend([str(recto_file), str(verso_file)])
        my_deck.add_note(my_note)

    package = genanki.Package(my_deck)
    package.media_files = package_files
    package.write_to_file(package_filename)
