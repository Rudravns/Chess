import sys
from Data_types import *
from Helper import SpriteSheet, scale
import pygame


class PieceType:
    
    PAWN = {
        "type": "pawn",
        "symbol": "P",
        "value": 1,
        "Position": None,
        "img": ImageType,
        "Color": ColorType,
    }

    KNIGHT = {
        "type": "knight",
        "symbol": "N",
        "value": 3,
        "Position":  None,
        "img": ImageType,
        "Color": ColorType,
    }

    BISHOP = {
        "type": "bishop",
        "symbol": "B",
        "value": 3,
        "Position":  None,
        "img": ImageType,
        "Color": ColorType,
    }

    ROOK = {
        "type": "rook",
        "symbol": "R",
        "value": 5,
        "Position":  None,
        "img": ImageType,
        "Color": ColorType,
    }

    QUEEN = {
        "type": "queen",
        "symbol": "Q",
        "value": 9,
        "Position":  None,
        "img": ImageType,
        "Color": ColorType,
    }

    KING = {
        "type": "king",
        "symbol": "K",
        "value": float("inf"),
        "Position":  None,
        "img": ImageType,
        "Color": ColorType,
        "can_castle_kingside": True,
        "can_castle_queenside": True
    }

def init():
    #setup SpriteSheet for pieces
    pieces_sprite_sheet = SpriteSheet("Chess_Pieces_SpriteSheet.png")
    pieces_images = pieces_sprite_sheet.extract_image(Crop_size=(640,695), Crop_start=(0, 0), Scale=(60, 60))
    PieceType.PAWN['img'] = pieces_images[5]
    PieceType.ROOK['img'] = pieces_images[4]
    PieceType.KNIGHT['img'] = pieces_images[3]
    PieceType.BISHOP['img'] = pieces_images[2]
    PieceType.QUEEN['img'] = pieces_images[1]
    PieceType.KING['img'] = pieces_images[0]

class PieceColor:
    WHITE = "white"
    BLACK = "black"

class Piece:
    def __init__(self, piece_type: dict, color: str):
        self.piece_type = piece_type.copy()
        self.color = color
        if color == PieceColor.BLACK:
            self.piece_type['img'] = self.piece_type['img'].to_black_piece().scale((60, 80))

    def __repr__(self):
        return f"{self.color.capitalize()} {self.piece_type['symbol']}"


if __name__ == "__main__":
    pygame.init()
    pygame.display.init()
    pygame.font.init()

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Chess_piece Test")
    init()
    pawn = Piece(PieceType.PAWN, PieceColor.BLACK)
    print(pawn)
    

    while True:
        screen.fill(LIGHT_ROSE)
        pawn.piece_type['img'].draw((100, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()