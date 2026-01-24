# Main.py
from matplotlib.pyplot import pie
import pygame
import sys,os
from Helper import *
from Data_types import *
import Pieces
import Notation


class App:
    def __init__(self):
        #pygame init
        pygame.init()
        pygame.display.init()
        pygame.font.init()

        #screen init
        self.last_width, self.last_height = 1000, 600
        self.screen = pygame.display.set_mode((self.last_width, self.last_height), pygame.RESIZABLE)
        pygame.display.set_caption("Chess")
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        
        #clock init
        self.clock = pygame.time.Clock()
        self.tick = 120  # FPS
        self.dt = 0.0

        #pieces init
        Pieces.init()
        self.board = Notation.parse_fen(START_FEN)
        self.pieces: list[list[Pieces.Piece | None]] = []
        self.Picked_up_piece: Pieces.Piece | None = None
        self.Turn = Pieces.PieceColor.WHITE


        for row in range(8):
            lane: list[Pieces.Piece | None] = []

            for col in range(8):
                piece_symbol = self.board[row][col]
                piece: Pieces.Piece | None = None

                if piece_symbol is not None:
                    color = (
                        Pieces.PieceColor.WHITE
                        if piece_symbol.isupper()
                        else Pieces.PieceColor.BLACK
                    )

                    symbol = piece_symbol.upper()

                    for pt in Pieces.PieceType.__dict__.values():
                        if isinstance(pt, dict) and pt["symbol"] == symbol:
                            piece = Pieces.Piece(pt, color)
                            piece.set_position(col, row)
                            break
                lane.append(piece)

           
            self.pieces.append(lane)

      
        
    def run(self):
        while True:
            self.dt = self.clock.tick(self.tick) / 1000
            self.screen.fill((0, 0, 0))

            # drawing
            self.draw_board(white_square_color=LIGHT_BROWN, black_square_color=DARK_BROWN)

            # text
            render_text(
                text=f"FPS: {round(self.clock.get_fps())}",
                position=(10, 10),
                size=36,
                color=(255, 255, 255)
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.VIDEORESIZE:
                    self.last_width, self.last_height = event.w, event.h
                    #self.screen = pygame.display.set_mode((self.last_width, self.last_height), pygame.RESIZABLE)
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_F11:
                       self.screen = pygame.display.set_mode(
                           get_fullscreen() if self.screen.get_size() != get_fullscreen() else (self.last_width, self.last_height),  
                           pygame.RESIZABLE)



            pygame.display.flip()

      
    def draw_board(self, white_square_color: ColorType, black_square_color: ColorType):
        h, w = self.screen.get_size()
        square_h = h // 8
        square_w = w // 8

        square_size = min(square_h, square_w)
        mouse_position = pygame.mouse.get_pos()
        Mouse_down = pygame.mouse.get_pressed()[0]
        
        piece_index = 0
        for row in range(8):
            for col in range(8):

                #Board display
                piece_location = self.pieces[row][col]
                rect = pygame.Rect(col * square_size, row * square_size, square_size, square_size)
                color = white_square_color if (row + col) % 2 == 0 else black_square_color
                pygame.draw.rect(
                    self.screen,
                    pygame.Color(color),
                    rect
                )

                

                #Piece display
                if piece_location:
                    piece = piece_location
                    img = piece.piece_type['img']
                    img = img.scale((square_size, square_size))
                    piece_index += 1
                    if rect.collidepoint(mouse_position) and Mouse_down and not self.Picked_up_piece and (piece.color == self.Turn):
                        self.Picked_up_piece = piece

                    if piece != self.Picked_up_piece:
                        img.draw((col * square_size, row * square_size))

        #Picked up piece display
        if self.Picked_up_piece :
            img = self.Picked_up_piece.piece_type['img']
            img = img.scale((square_size, square_size))
            img.draw((mouse_position[0] - square_size // 2, mouse_position[1] - square_size // 2))

        #Piece Pickup Disable(Drop Logic)
        if not Mouse_down and self.Picked_up_piece:
            new_col = int(mouse_position[0] // square_size)
            new_row = int(mouse_position[1] // square_size)

            old_col = self.Picked_up_piece.col
            old_row = self.Picked_up_piece.row

            # Check board bounds
            if 0 <= new_col < 8 and 0 <= new_row < 8:
                # Ignore drop on same square
                if (new_col, new_row) != (old_col, old_row):

                    target_piece = self.pieces[new_row][new_col]

                    # Allow move if square is empty OR enemy piece (capture)
                    if target_piece is None or target_piece.color != self.Picked_up_piece.color:
                        # Remove piece from old square
                        self.pieces[old_row][old_col] = None

                        # Capture (overwrite) target square
                        self.pieces[new_row][new_col] = self.Picked_up_piece
                        self.Picked_up_piece.set_position(new_col, new_row)

                        # Switch turn ONLY after a valid move
                        self.Turn = (
                            Pieces.PieceColor.BLACK
                            if self.Turn == Pieces.PieceColor.WHITE
                            else Pieces.PieceColor.WHITE
                        )

            # Always release the piece after mouse up
            self.Picked_up_piece = None

                
                


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    app = App()
    app.run()
