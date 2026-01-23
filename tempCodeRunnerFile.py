import sys
from Data_types import *
from Helper import SpriteSheet, scale
import pygame





class PieceType:
    #setup SpriteSheet for pieces
    pieces_sprite_sheet = SpriteSheet("Chess_Pieces_SpriteSheet.png")
    pieces_images = pieces_sprite_sheet.extract_image(Crop_size=(640,695), Crop_start=(0, 0), Scale=(60, 60))
    PAWN = {
        "type": "pawn",
        "symbol": "P",
        "value": 1,
        "Position": None,
        "img": pieces_images[5]  #Pawn image
    }

    KNIGHT = {
        "type": "knight",
        "symbol": "N",
        "value": 3,
        "Position":  None,
        "img": pieces_images[3]  #Knight image  
    }

    BISHOP = {
        "type": "bishop",
        "symbol": "B",
        "value": 3,
        "Position":  None,
        "img": pieces_images[2]  #Bishop image
    }

    ROOK = {
        "type": "rook",
        "symbol": "R",
        "value": 5,
        "Position":  None,
        "img": pieces_images[4]  #Rook image
    }

    QUEEN = {
        "type": "queen",
        "symbol": "Q",
        "value": 9,
        "Position":  None,
        "img": pieces_images[1]  #Queen image
    }

    KING = {
        "type": "king",
        "symbol": "K",
        "value": float("inf"),
        "Position":  None,
        "img": pieces_images[0],  #King image
        "can_castle_kingside": True,
        "can_castle_queenside": True
    }


class PieceColor:
    WHITE = "white"
    BLACK = "black"


class Piece:
    def __init__(self, piece_type: dict, color: str):
        self.piece_type = piece_type
        self.color = color

    def __repr__(self):
        return f"{self.color.capitalize()} {self.piece_type['symbol']}"

if __name__ == "__main__":
    pygame.init()
    pygame.display.init()
    pygame.font.init()

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Chess_piece Test")
    
    pawn = Piece(PieceType.PAWN, PieceColor.WHITE)
    print(pawn)
    

    while True:
        screen.fill(LIGHT_ROSE)
        screen.blit(pawn.piece_type['img'], (100, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()