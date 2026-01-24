from re import S
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

def parse_fen_full(fen: str) -> Tuple[List[List[Optional[str]]], str, str, str, int, int, str]:
    """Parse a full FEN string into its components."""
    parts = fen.split(' ')
    board = parse_fen(fen)
    turn = parts[1]
    castling = parts[2]
    en_passant = parts[3]
    halfmove_clock = int(parts[4])
    fullmove_number = int(parts[5])
    promotion = parts[6] if len(parts) > 6 else ""

    return board, turn, castling, en_passant, halfmove_clock, fullmove_number, promotion

def generate_fen(board: List[List[Optional[str]]], turn: str, castling: str, en_passant: str, halfmove_clock: int, fullmove_number: int, promotion: str) -> str:
    """Generate a FEN string from a 2D board representation."""
    fen:str = ""

    for row in board:
        empty_count = 0
        for cell in row:
            if cell is None:
                empty_count += 1
            else:
                if empty_count > 0:
                    fen += str(empty_count)
                    empty_count = 0
                fen += cell
        if empty_count > 0:
            fen += str(empty_count)
        fen += '/'

    return f"{fen.rstrip('/')} {turn} {castling} {en_passant} {halfmove_clock} {fullmove_number}"


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


#====================================================
# Game Notations
#====================================================
Black_moves:int = parse_fen_full(START_FEN)[4]
White_moves:int = parse_fen_full(START_FEN)[5]

if __name__ == "__main__":
    #START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = parse_fen(START_FEN)
    for row in board:
        print(row)
        pass
    print(generate_fen(board, "w", "KQkq", "-", 0, 1, ""))