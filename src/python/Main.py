# Main.py
import pygame
import sys,os
from Helper import *
from Data_types import *
import Pieces
import Notation
import Translate


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
        self.Fen = START_FEN


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

        #promotion square 
        self.awaiting_promotion = False
        self.promotion_pawn = None
        witdh, hieght = scale((300,100))
        w,h = self.last_width/2-witdh/2, self.last_height/2-hieght/2
        self.promotion_Display_Data = {
            "rect": pygame.Rect(w,h, witdh, hieght),

            "White Queen": Pieces.Piece(Pieces.PieceType.QUEEN,Pieces.PieceColor.WHITE),
            "White Rook": Pieces.Piece(Pieces.PieceType.ROOK,Pieces.PieceColor.WHITE),
            "White Knight": Pieces.Piece(Pieces.PieceType.KNIGHT,Pieces.PieceColor.WHITE),
            "White Bishop": Pieces.Piece(Pieces.PieceType.BISHOP,Pieces.PieceColor.WHITE),
            

            "Black Queen": Pieces.Piece(Pieces.PieceType.QUEEN,Pieces.PieceColor.BLACK),
            "Black Rook": Pieces.Piece(Pieces.PieceType.ROOK,Pieces.PieceColor.BLACK),
            "Black Knight": Pieces.Piece(Pieces.PieceType.KNIGHT,Pieces.PieceColor.BLACK),
            "Black Bishop": Pieces.Piece(Pieces.PieceType.BISHOP,Pieces.PieceColor.BLACK),

            "Queen Rect": pygame.Rect(w, h, *scale((75,105))),
            "Rook Rect": pygame.Rect(w+scale(75), h, *scale((75,95))),
            "Knight Rect": pygame.Rect(w+scale(150), h, *scale((75,100))),
            "Bishop Rect": pygame.Rect(w+scale(225), h, *scale((75,100))),

            
        }
        
    def run(self):
        while True:
            self.dt = self.clock.tick(self.tick) / 1000
            self.screen.fill((0, 0, 0))

            # drawing
            self.update_board(white_square_color=LIGHT_BROWN, black_square_color=DARK_BROWN)

            # text
            render_text(
                text=f"FPS: {round(self.clock.get_fps())}",
                position=(10, 10),
                size=36,
                color=(255, 255, 255)
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print(self.Fen)
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.VIDEORESIZE:
                    self.last_width, self.last_height = event.w, event.h
                    #self.screen = pygame.display.set_mode((self.last_width, self.last_height), pygame.RESIZABLE)
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print(self.Fen)
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_F11:
                       self.screen = pygame.display.set_mode(
                           get_fullscreen() if self.screen.get_size() != get_fullscreen() else (self.last_width, self.last_height),  
                           pygame.RESIZABLE)


            self.Fen = Notation.generate_fen(self.board, self.Turn, "KQkq", Notation.en_passant_square, Notation.Black_moves, Notation.White_moves, "")
            pygame.display.flip()
      
    def update_board(self, white_square_color: ColorType, black_square_color: ColorType):
        h, w = self.screen.get_size()
        square_size = min(h // 8, w // 8)

        mouse_pos = pygame.mouse.get_pos()
        mouse_down = pygame.mouse.get_pressed()[0]

        # Sync engine board
        Translate.engine.SetBoardFromFEN(self.Fen)

        # -------------------------------------------------
        # PROMOTION UI (BLOCK GAME)
        # -------------------------------------------------
        if self.awaiting_promotion:
            self.draw_board_only(white_square_color, black_square_color, square_size)
            self.draw_prom_display()

            if mouse_down:
                promoted_piece = self.handle_promotion_click(mouse_pos)
                if promoted_piece:
                    r = self.promotion_pawn.row # pyright: ignore[reportOptionalMemberAccess]
                    c = self.promotion_pawn.col # pyright: ignore[reportOptionalMemberAccess]

                    promoted_piece.set_position(c, r)
                    self.pieces[r][c] = promoted_piece
                    self.board[r][c] = promoted_piece.piece_type["symbol"] if promoted_piece.color == Pieces.PieceColor.WHITE else promoted_piece.piece_type["symbol"].lower()

                    self.awaiting_promotion = False
                    self.promotion_pawn = None

                    # Switch turn AFTER promotion
                    self.Turn = (
                        Pieces.PieceColor.BLACK
                        if self.Turn == Pieces.PieceColor.WHITE
                        else Pieces.PieceColor.WHITE
                    )
            return

        # -------------------------------------------------
        # Get legal moves
        # -------------------------------------------------
        legal_moves = []
        if self.Picked_up_piece:
            moves = Translate.engine.GetLegalMoves(
                self.Picked_up_piece.col,
                self.Picked_up_piece.row
            )
            legal_moves = [(m.Item1, m.Item2) for m in moves]

        # -------------------------------------------------
        # Draw board + pieces
        # -------------------------------------------------
        for row in range(8):
            for col in range(8):
                rect = pygame.Rect(
                    col * square_size,
                    row * square_size,
                    square_size,
                    square_size
                )

                color = white_square_color if (row + col) % 2 == 0 else black_square_color
                pygame.draw.rect(self.screen, pygame.Color(color), rect)

                if (col, row) in legal_moves:
                    pygame.draw.circle(
                        self.screen,
                        GREY,
                        rect.center,
                        square_size // 6
                    )

                piece = self.pieces[row][col]
                if piece:
                    if (
                        rect.collidepoint(mouse_pos)
                        and mouse_down
                        and not self.Picked_up_piece
                        and piece.color == self.Turn
                    ):
                        self.Picked_up_piece = piece

                    if piece != self.Picked_up_piece:
                        img = piece.piece_type["img"].scale((square_size, square_size))
                        img.draw(rect.topleft)

        # -------------------------------------------------
        # Draw picked piece
        # -------------------------------------------------
        if self.Picked_up_piece:
            img = self.Picked_up_piece.piece_type["img"].scale((square_size, square_size))
            img.draw((
                mouse_pos[0] - square_size // 2,
                mouse_pos[1] - square_size // 2
            ))

        # -------------------------------------------------
        # Drop logic
        # -------------------------------------------------
        if not mouse_down and self.Picked_up_piece:
            old_col = self.Picked_up_piece.col
            old_row = self.Picked_up_piece.row
            new_col = mouse_pos[0] // square_size
            new_row = mouse_pos[1] // square_size

            if (new_col, new_row) in legal_moves:
                # EN PASSANT
                if (
                    self.board[old_row][old_col].lower() == "p" # pyright: ignore[reportOptionalMemberAccess]
                    and self.board[new_row][new_col] is None
                    and new_col != old_col
                ):
                    self.pieces[old_row][new_col] = None
                    self.board[old_row][new_col] = None

                # Move
                self.pieces[old_row][old_col] = None
                self.pieces[new_row][new_col] = self.Picked_up_piece
                self.board[new_row][new_col] = self.board[old_row][old_col]
                self.board[old_row][old_col] = None
                self.Picked_up_piece.set_position(new_col, new_row)

                # CASTLING
                if self.Picked_up_piece.piece_type["type"] == "king":
                    if new_col - old_col == 2 and self.Picked_up_piece.piece_type["can_castle_queenside"]:
                        rook = self.pieces[old_row][7]
                        self.pieces[old_row][5] = rook
                        self.pieces[old_row][7] = None
                        rook.set_position(5, old_row) # pyright: ignore[reportOptionalMemberAccess]
                    elif new_col - old_col == -2 and self.Picked_up_piece.piece_type["can_castle_kingside"]:
                        rook = self.pieces[old_row][0]
                        self.pieces[old_row][3] = rook
                        self.pieces[old_row][0] = None
                        rook.set_position(3, old_row)   # pyright: ignore[reportOptionalMemberAccess]

                # PAWN PROMOTION
                if (
                    self.Picked_up_piece.piece_type["type"] == "pawn"
                    and (new_row == 0 or new_row == 7)
                ):
                    self.awaiting_promotion = True
                    self.promotion_pawn = self.Picked_up_piece
                    self.Picked_up_piece = None
                    return

                # Switch turn
                self.Turn = (
                    Pieces.PieceColor.BLACK
                    if self.Turn == Pieces.PieceColor.WHITE
                    else Pieces.PieceColor.WHITE
                )

            self.Picked_up_piece = None

    def draw_board_only(self, white_square_color, black_square_color, square_size):
        king_pos = None

        # Find king position
        for row in self.pieces:
            for p in row:
                if p and p.piece_type['type'] == 'king' and p.color == self.Turn:
                    king_pos = (p.col, p.row)
                    break

        for row in range(8):
            for col in range(8):
                rect = pygame.Rect(col*square_size, row*square_size, square_size, square_size)

                base_color = white_square_color if (row + col) % 2 == 0 else black_square_color

                # Only highlight king square if in check
                if king_pos == (col, row) and self.is_in_check(self.Turn):
                    color = CHECK
                else:
                    color = base_color

                pygame.draw.rect(self.screen, pygame.Color(color), rect)

                piece = self.pieces[row][col]
                if piece:
                    img = piece.piece_type["img"].scale((square_size, square_size))
                    img.draw(rect.topleft)


    def is_in_check(self, color):
        king = None
        for row in self.pieces:
            for p in row:
                if p and p.piece_type['type'] == 'king' and p.color == color:
                    king = p
                    break
        if king is None:
            return False
        check = Translate.engine.SquareUnderAttack(king.col, king.row, king.color == Pieces.PieceColor.WHITE)
        #if check: pygame.draw.rect(self.screen, CHECK, ())
        return check

    def is_checkmate(self, color):
        if not self.is_in_check(color):
            return False
        for row in range(8):
            for col in range(8):
                piece = self.pieces[row][col]
                if piece and piece.color == color:
                    moves = Translate.engine.GetLegalMoves(col, row)
                    if moves:
                        return False
        return True

    def draw_prom_display(self):
        data = self.promotion_Display_Data
        mouse_pos = pygame.mouse.get_pos()
        screen = self.screen

        # -------- Dim background --------
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill(pygame.Color(PROMO_BG_OVERLAY))
        screen.blit(overlay, (0, 0))


        # -------- Main panel --------
        pygame.draw.rect(
            screen,
            pygame.Color(PROMO_PANEL),
            data["rect"],
            border_radius=14
        )

        pygame.draw.rect(
            screen,
            pygame.Color(PROMO_BORDER),
            data["rect"],
            width=2,
            border_radius=14
        )

        # -------- Title (manually centered) --------
        title_surf, title_rect = render_text(
            "Choose Promotion",
            (0, 0),
            size=28,
            color=PROMO_TEXT,
            bold=True,
            draw=False
        )

        title_rect.centerx = data["rect"].centerx
        title_rect.bottom = data["rect"].top - scale(10)
        screen.blit(title_surf, title_rect)

        color_prefix = "White" if self.Turn == Pieces.PieceColor.WHITE else "Black"

        options = [
            ("Queen", data["Queen Rect"]),
            ("Rook", data["Rook Rect"]),
            ("Knight", data["Knight Rect"]),
            ("Bishop", data["Bishop Rect"]),
        ]

        for name, rect in options:
            hovered = rect.collidepoint(mouse_pos)

            # Option background
            pygame.draw.rect(
                screen,
                pygame.Color(PROMO_OPTION_HOVER if hovered else PROMO_OPTION),
                rect,
                border_radius=10
            )

            pygame.draw.rect(
                screen,
                pygame.Color(PROMO_BORDER),
                rect,
                width=1,
                border_radius=10
            )

            # Piece image
            piece = data[f"{color_prefix} {name}"]
            img_size = int(rect.width * (0.9 if hovered else 0.82))
            img = piece.piece_type["img"].scale((img_size, img_size))

            img_pos = (
                rect.centerx - img_size // 2,
                rect.centery - img_size // 2 - scale(8)
            )
            img.draw(img_pos)

            # Label under icon
            label_surf, label_rect = render_text(
                name,
                (0, 0),
                size=18,
                color=PROMO_TEXT,
                draw=False
            )

            label_rect.centerx = rect.centerx
            label_rect.top = rect.bottom - scale(22)
            screen.blit(label_surf, label_rect)

    def handle_promotion_click(self, mouse_pos):
        if not pygame.mouse.get_pressed()[0]:
            return None

        data = self.promotion_Display_Data
        color_prefix = "White" if self.Turn == Pieces.PieceColor.WHITE else "Black"

        for name in ["Queen", "Rook", "Knight", "Bishop"]:
            if data[f"{name} Rect"].collidepoint(mouse_pos):
                pygame.time.delay(120)
                return data[f"{color_prefix} {name}"]

        return None



if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    app = App()
    app.run()
