from typing import * # pyright: ignore[reportWildcardImportFromLibrary]
from Data_types import *
from Helper import *
from Pieces import *
import pygame


#=====================================================
# FEN Parsing
#=====================================================
def parse_fen(fen: str) -> List[List[Optional[str]]]:
    """Parse a FEN string into a 2D board representation."""
    board: List[List[Optional[str]]] = []
    rows = fen.split(' ')[0].split('/')

    for row in rows:
        board_row: List[Optional[str]] = []
        for char in row:
            if char.isdigit():
                for _ in range(int(char)):
                    board_row.append(None)
            else:
                board_row.append(char)
        board.append(board_row)

    return board


def convert_position_to_notation(col: int, row: int) -> str:
    """Convert board coordinates to standard chess notation."""
    files = 'abcdefgh'
    ranks = '87654321'
    return f"{files[col]}{ranks[row]}"

def convert_notation_to_position(notation: PiecePosition) -> Position:
    """Convert standard chess notation to board coordinates."""
    files = 'abcdefgh'
    ranks = '87654321'
    col = files.index(notation[0])
    row = ranks.index(str(notation[1]))
    return (col, row)


if __name__ == "__main__":
    board = parse_fen(START_FEN)
    for row in board:
        print(row)
