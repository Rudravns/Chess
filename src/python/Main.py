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
        pygame.display.set_icon(load_image("icon.png"))
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.settings = get_data("settings")
        #clock init
        self.clock = pygame.time.Clock()
        self.tick = self.settings["fps"]  # FPS
        self.dt = 0.0

        #pieces init
        Pieces.init()
        self.game_num = self.settings["games played"]
        
        self.game_data = get_game_data(game_num=self.game_num)
        self.pieces: list[list[Pieces.Piece | None]] = []
        self.Picked_up_piece: Pieces.Piece | None = None
        self.Fen = self.game_data["FEN"]
        self.FENS = self.game_data["FENS"]
        self.PGN = self.game_data["PGN"]
        self.move_pgn = []
        self.pgn_scroll_y = 0
        self.move_counter = 1
        # FIX: Set move_counter based on existing PGN data
        if self.PGN:
            # Get the highest move number currently in the dictionary
            existing_moves = [int(k) for k in self.PGN.keys()]
            if existing_moves:
                max_move = max(existing_moves)
                # If Black hasn't moved yet in the last turn, we are still on that move number
                if len(self.PGN[str(max_move)]) < 2:
                    self.move_counter = max_move
                else:
                    self.move_counter = max_move + 1
            else:
                self.move_counter = 1
        else:
            self.move_counter = 1

        self.Turn = Pieces.PieceColor.WHITE if Notation.parse_fen_full(self.Fen)[1] == 'w' else Pieces.PieceColor.BLACK
        self.board = Notation.parse_fen(self.Fen)
        Translate.engine.SetBoardFromFEN(self.Fen)
        print(self.Fen)
        
        



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
            if self.settings["Console debug"]:os.system('cls' if os.name == 'nt' else 'clear') 
            self.dt = self.clock.tick(self.tick) / 1000
            self.screen.fill((0, 0, 0))

            # drawing
            board_color = get_color(self.settings["Board style"])
            h, w = self.screen.get_size()
            square_size = min(h // 8, w // 8)

            self.update_board(white_square_color=board_color[0], black_square_color=board_color[1])
            self.draw_pgn(square_size)
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
                       
                # MOUSE WHEEL SCROLLING
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4: # Scroll Up
                        self.pgn_scroll_y += 20
                    if event.button == 5: # Scroll Down
                        self.pgn_scroll_y -= 20
                    
            pygame.display.flip()
      
    def update_board(self, white_square_color: ColorType, black_square_color: ColorType):
        h, w = self.screen.get_size()
        square_size = min(h // 8, w // 8)

        mouse_pos = pygame.mouse.get_pos()
        mouse_down = pygame.mouse.get_pressed()[0]

        

        # -------------------------------------------------
        # PROMOTION UI (BLOCK GAME)
        # -------------------------------------------------
        if self.awaiting_promotion:
            self.draw_board_only(white_square_color, black_square_color, square_size)
            self.draw_prom_display()

            if mouse_down:
                promoted_piece = self.handle_promotion_click(mouse_pos)
                if promoted_piece:
                    r = self.promotion_pawn.row  # pyright: ignore[reportOptionalMemberAccess]
                    c = self.promotion_pawn.col # pyright: ignore[reportOptionalMemberAccess]

                    promoted_piece.set_position(c, r)
                    self.pieces[r][c] = promoted_piece
                    # Update the board array symbol
                    self.board[r][c] = promoted_piece.piece_type["symbol"] if promoted_piece.color == Pieces.PieceColor.WHITE else promoted_piece.piece_type["symbol"].lower()
                    
                    if self.move_pgn:
                        self.move_pgn[-1] += "=" + promoted_piece.piece_type["symbol"].upper()

                    self.awaiting_promotion = False
                    self.promotion_pawn = None

                    # 🔹 ADD THIS: Tell the engine about the new Queen/Rook/etc.
                    self.update_fen("-") 

                    # Switch turn AFTER promotion and engine update
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

        #console edition 
        if self.settings["Console debug"]:
            print(self.is_in_check(self.Turn))
            print(self.Turn, '\n')
            [print(x) for x in self.board]



        # REMINDER: white = BIG
        #           black = SMALL
        # Make sure rook is there for the king to castle
        
        #starting with White king  


        if self.Turn == Pieces.PieceColor.WHITE:
            white_king_pos = Notation.find_piece(self.board, 'K')
            white_king = self.pieces[white_king_pos[0]][white_king_pos[1]]  # pyright: ignore[reportOptionalSubscript]
            
            if not self.board[7][0] == 'R':
                white_king.piece_type["CanCastleQueenside"] = False # pyright: ignore[reportOptionalMemberAccess]
                Translate.engine.DisableCastling(True, False)
            if not self.board[7][7] == 'R':
                white_king.piece_type["CanCastleKingside"] = False # pyright: ignore[reportOptionalMemberAccess]
                Translate.engine.DisableCastling(True, True)

        #now black king
        if self.Turn == Pieces.PieceColor.BLACK:
            black_king_pos = Notation.find_piece(self.board, 'k')
            black_king = self.pieces[black_king_pos[0]][black_king_pos[1]] # pyright: ignore[reportOptionalSubscript]
            if not self.board[0][0] == 'r':
                black_king.piece_type["CanCastleQueenside"] = False   # pyright: ignore[reportOptionalMemberAccess]
            Translate.engine.DisableCastling(False, False)
            if not self.board[0][7] == 'r':
                black_king.piece_type["CanCastleKingside"] = False  # pyright: ignore[reportOptionalMemberAccess]   
                Translate.engine.DisableCastling(False, True)



              
                


        for row in range(8):
            for col in range(8):
                rect = pygame.Rect(
                    col * square_size,
                    row * square_size,
                    square_size,
                    square_size
                )

                color = white_square_color if (row + col) % 2 == 0 else black_square_color
                

                if self.is_in_check(self.Turn): # pyright: ignore[reportOptionalMemberAccess]
                    if self.board[row][col] == "k" and self.Turn == Pieces.PieceColor.BLACK:
                        color = CHECK
                    elif self.board[row][col] == "K" and self.Turn == Pieces.PieceColor.WHITE:
                        color = CHECK
                
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
        # Inside update_board's "Drop logic" in Main.py
        if not mouse_down and self.Picked_up_piece:
            old_col = self.Picked_up_piece.col
            old_row = self.Picked_up_piece.row
            new_col = mouse_pos[0] // square_size
            new_row = mouse_pos[1] // square_size

            if (new_col, new_row) in legal_moves:
                # Check for double pawn push to set En Passant square
                ep_square = "-"
                if self.Picked_up_piece.piece_type["type"] == "pawn":
                    if abs(new_row - old_row) == 2:
                        # The square skipped over is the EP target
                        ep_rank = 8 - (old_row + new_row) // 2
                        ep_file = chr(ord('a') + new_col)
                        ep_square = f"{ep_file}{ep_rank}"
                        Notation.en_passant_square = ep_square # Update your global notation
                    
                    # Handle the actual capture of the pawn in En Passant
                    # If moving diagonally to an empty square, it's en passant
                    if old_col != new_col and self.board[new_row][new_col] is None:
                        capture_row = old_row
                        self.pieces[capture_row][new_col] = None
                        self.board[capture_row][new_col] = None

                # Move
                #first update PGN
                # --- Inside update_board's "Drop logic" ---
        if not mouse_down and self.Picked_up_piece:
            old_col = self.Picked_up_piece.col
            old_row = self.Picked_up_piece.row
            new_col = mouse_pos[0] // square_size
            new_row = mouse_pos[1] // square_size

            if (new_col, new_row) in legal_moves:
                # ... (Keep your En Passant logic here) ...

                # --- NEW PGN GENERATION WITH CHECK DETECTION ---
                pgn = ""
                piece_symbol = self.board[old_row][old_col]
                target_piece = self.board[new_row][new_col]
                target_square = Notation.convert_position_to_notation(new_col, new_row)
                start_square = Notation.convert_position_to_notation(old_col, old_row)

                if piece_symbol.upper() == 'K' and abs(old_col - new_col) == 2: # pyright: ignore[reportOptionalMemberAccess]
                    pgn = "O-O" if new_col > old_col else "O-O-O"
                else:
                    if piece_symbol.upper() != 'P': pgn += piece_symbol.upper() # pyright: ignore[reportOptionalMemberAccess]
                    is_capture = target_piece is not None or (piece_symbol.upper() == 'P' and old_col != new_col) # pyright: ignore[reportOptionalMemberAccess]
                    if is_capture:
                        if piece_symbol.upper() == 'P': pgn += start_square[0] # pyright: ignore[reportOptionalMemberAccess]
                        pgn += "x"
                    pgn += target_square
                
                self.move_pgn.append(pgn)

                # --- Now finalize the move ---
                self.pieces[old_row][old_col] = None
                self.pieces[new_row][new_col] = self.Picked_up_piece
                self.board[new_row][new_col] = self.board[old_row][old_col]
                self.board[old_row][old_col] = None
                self.Picked_up_piece.set_position(new_col, new_row)

                
                

                # CASTLING
                if self.Picked_up_piece.piece_type["type"] == "king":
                    
                    
                    
                    if abs(old_col - new_col) == 2:

                        if old_col > new_col and self.Picked_up_piece.piece_type["can_castle_queenside"]:
                            rook = self.pieces[old_row][0]
                            rook.set_position(3, old_row) # pyright: ignore[reportOptionalMemberAccess]
                            self.pieces[old_row][3] = rook
                            self.board[old_row][0] = None
                            self.pieces[old_row][0] = None
                            self.board[old_row][3] = "R" if self.Picked_up_piece.color == Pieces.PieceColor.WHITE else "r"
                            
                        elif old_col < new_col and self.Picked_up_piece.piece_type["can_castle_kingside"]:
                            rook = self.pieces[old_row][7]
                            rook.set_position(5, old_row) # pyright: ignore[reportOptionalMemberAccess] 
                            self.pieces[old_row][5] = rook
                            self.board[old_row][7] = None
                            self.pieces[old_row][7] = None
                            self.board[old_row][5] = "R" if self.Picked_up_piece.color == Pieces.PieceColor.WHITE else "r"
                            
                    self.Picked_up_piece.piece_type["can_castle_kingside"] = False
                    self.Picked_up_piece.piece_type["can_castle_queenside"] = False
                    Translate.engine.DisableCastling(True, True) if self.Picked_up_piece.color == Pieces.PieceColor.WHITE else Translate.engine.DisableCastling(False, True)
                    Translate.engine.DisableCastling(True, False) if self.Picked_up_piece.color == Pieces.PieceColor.WHITE else Translate.engine.DisableCastling(False, False)
                              

                # PAWN PROMOTION
                if (
                    self.Picked_up_piece.piece_type["type"] == "pawn"
                    and (new_row == 0 or new_row == 7)
                ):
                    self.awaiting_promotion = True
                    self.promotion_pawn = self.Picked_up_piece
                    self.Picked_up_piece = None
                    return
                
                self.update_fen(ep_square)

                # Switch turn
                self.Turn = (
                    Pieces.PieceColor.BLACK
                    if self.Turn == Pieces.PieceColor.WHITE
                    else Pieces.PieceColor.WHITE
                )

            self.Picked_up_piece = None

    def draw_board_only(self, white_square_color, black_square_color, square_size):
    

        for row in range(8):
            for col in range(8):
                rect = pygame.Rect(col*square_size, row*square_size, square_size, square_size)

                color = white_square_color if (row + col) % 2 == 0 else black_square_color

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

    def update_fen(self, move_ep_square):
        # Logic for turn increment
        if self.Turn == Pieces.PieceColor.WHITE:
            Notation.White_moves += 1
        else:
            Notation.Black_moves += 1





        white_king_pos = Notation.find_piece(self.board, 'K') 
        white_king = self.pieces[white_king_pos[0]][white_king_pos[1]]  # pyright: ignore[reportOptionalSubscript]

        black_king_pos = Notation.find_piece(self.board, 'k')
        black_king = self.pieces[black_king_pos[0]][black_king_pos[1]] # pyright: ignore[reportOptionalSubscript]

        castle = ""
        if white_king.piece_type["can_castle_kingside"]: # pyright: ignore[reportOptionalMemberAccess]
            castle += "K"
        if white_king.piece_type["can_castle_queenside"]: # pyright: ignore[reportOptionalMemberAccess]
            castle += "Q"
        if black_king.piece_type["can_castle_kingside"]: # pyright: ignore[reportOptionalMemberAccess]
            castle += "k"   
        if black_king.piece_type["can_castle_queenside"]: # pyright: ignore[reportOptionalMemberAccess]
            castle += "q"
        if castle == "":
            castle = "-"
        
        
        current_ep = move_ep_square 
    
        # Generate the FEN with the new EP square
        self.Fen = Notation.generate_fen(
            self.board, 
            ('b' if self.Turn == Pieces.PieceColor.WHITE else 'w'), 
            castle, 
            current_ep, # This is the key!
            Notation.Black_moves, 
            Notation.White_moves, 
            ""
        )
        # Reset the global tracker so the next move doesn't accidentally reuse it
        Notation.en_passant_square = "-" 
        #print(self.Fen)
        
        self.FENS.append(self.Fen)
        Translate.engine.SetBoardFromFEN(self.Fen)

        # Check for check/checkmate
        opp_color = Pieces.PieceColor.BLACK if self.Turn == Pieces.PieceColor.WHITE else Pieces.PieceColor.WHITE
        suffix = ""
        if self.is_checkmate(opp_color):
            suffix = "#"
        elif self.is_in_check(opp_color):
            suffix = "+"
        
        if self.move_pgn:
            self.move_pgn[-1] += suffix

        m_key = str(self.move_counter)
        if m_key not in self.PGN:
            self.PGN[m_key] = []

        if self.move_pgn:
            new_move = self.move_pgn[-1]
            if len(self.PGN[m_key]) < (1 if self.Turn == Pieces.PieceColor.WHITE else 2):
                self.PGN[m_key].append(new_move)

        if self.Turn == Pieces.PieceColor.BLACK:
            self.move_counter += 1
            self.move_pgn = []

        self.game_data["FEN"] = self.Fen
        self.game_data["FENS"] = self.FENS
        self.game_data["White won"] = (suffix == "#" and self.Turn == Pieces.PieceColor.WHITE)
        self.game_data["Black won"] = (suffix == "#" and self.Turn == Pieces.PieceColor.BLACK)
        self.game_data["PGN"] = self.PGN

        # Auto-scroll to bottom on new move
        self.pgn_scroll_y = -100000
        
        save_game(self.game_data, self.game_num)

    def rollback(self, move_num, color_idx):
        """
        Revert game state to a specific move.
        move_num: The move number (key in PGN).
        color_idx: 0 for White, 1 for Black.
        """
        # Calculate index in FENS list
        # FENS[0] is start. FENS[1] is after White move 1. FENS[2] is after Black move 1.
        fen_index = (move_num * 2) - 1 + color_idx
        
        if fen_index >= len(self.FENS):
            return

        # 1. Slice FENS history
        self.FENS = self.FENS[:fen_index+1]
        self.Fen = self.FENS[-1]
        
        # 2. Slice PGN history
        # Remove all keys greater than the selected move number
        keys_to_remove = [k for k in self.PGN.keys() if int(k) > move_num]
        for k in keys_to_remove:
            del self.PGN[k]
            
        # If we rolled back to White's move, remove Black's move from this entry
        if color_idx == 0:
            if str(move_num) in self.PGN:
                self.PGN[str(move_num)] = [self.PGN[str(move_num)][0]]
        
        # 3. Restore Board State
        self.board = Notation.parse_fen(self.Fen)
        
        # 4. Reset Engine (to restore castling rights which default to True on new engine)
        Translate.engine = Translate.load_engine()
        Translate.engine.SetBoardFromFEN(self.Fen)
        
        # 5. Parse FEN to restore variables
        _, turn_char, castling, ep, half, full, _ = Notation.parse_fen_full(self.Fen)
        
        self.Turn = Pieces.PieceColor.WHITE if turn_char == 'w' else Pieces.PieceColor.BLACK
        Notation.White_moves = full
        Notation.Black_moves = half
        Notation.en_passant_square = ep
        
        # Sync Engine Castling Rights with FEN
        if 'K' not in castling: Translate.engine.DisableCastling(True, True)
        if 'Q' not in castling: Translate.engine.DisableCastling(True, False)
        if 'k' not in castling: Translate.engine.DisableCastling(False, True)
        if 'q' not in castling: Translate.engine.DisableCastling(False, False)

        # 6. Rebuild Pieces Objects
        self.pieces = []
        self.init_pieces_from_board() # Helper function we will create/use logic from init

        # 7. Reset counters
        self.move_counter = move_num if color_idx == 0 else move_num + 1
        self.move_pgn = []
        self.Picked_up_piece = None
        self.awaiting_promotion = False

    def draw_pgn(self, square_size):
        # 1. Setup dimensions
        panel_x = square_size * 8 + scale(20)
        panel_y = scale(60) # Pushed down to leave room for header
        panel_width = self.screen.get_width() - panel_x - scale(20)
        panel_height = self.screen.get_height() - panel_y - scale(40)
        
        if panel_width < scale(150): return

        # Draw Background Box
        full_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(self.screen, (25, 25, 25), full_rect, border_radius=5)
        
        # Header (static, above the scrolling box)
        render_text("Move History", (panel_x, panel_y - scale(35)), size=24, color=(200, 200, 200), bold=True)

        # 2. Setup Clipping (This prevents text from bleeding out of the box)
        # We define the inner area where moves are visible
        move_clip_rect = pygame.Rect(panel_x + 5, panel_y + 10, panel_width - 10, panel_height - 20)
        self.screen.set_clip(move_clip_rect)

        line_height = scale(30)
        
        # Clamp scrolling
        total_height = len(self.PGN) * line_height
        view_height = panel_height - 20
        min_scroll = min(0, view_height - total_height)
        self.pgn_scroll_y = max(min_scroll, min(0, self.pgn_scroll_y))

        # Start drawing based on scroll offset
        start_y = panel_y + 10 + self.pgn_scroll_y
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        # 3. Draw the PGN moves
        # self.PGN is a dict: {"0": ["e4", "e5"], "1": ["d4", "d5"]}
        sorted_moves = sorted(self.PGN.keys(), key=lambda x: int(x))

        for move_idx in sorted_moves:
            moves = self.PGN[move_idx]
            
            # Subtract 1 so move #1 starts at index 0 for Y-coordinate math
            display_row = int(move_idx) - 1
            row_y = start_y + (display_row * line_height)
            
            # Optimization: Don't render if off screen
            if row_y < panel_y - line_height or row_y > panel_y + panel_height:
                continue

            # Move Number
            render_text(f"{move_idx}.", (panel_x + scale(10), row_y), size=int(scale(20)), color=(100, 100, 100))
            
            # White Move (Clean string)
            if len(moves) > 0:
                # Ensure we handle if the move is stored as a list accidentally
                txt = moves[0] if isinstance(moves[0], str) else str(moves[0])
                surf, rect = render_text(txt, (panel_x + scale(50), row_y), size=int(scale(20)), color=(255, 255, 255), draw=False)
                
                # Interaction
                if rect.collidepoint(mouse_pos):
                    pygame.draw.rect(self.screen, (70, 70, 70), rect, border_radius=3)
                    if mouse_click:
                        self.rollback(int(move_idx), 0)
                        self.screen.set_clip(None)
                        return
                
                self.screen.blit(surf, rect)
            
            # Black Move (Clean string)
            if len(moves) > 1:
                txt = moves[1] if isinstance(moves[1], str) else str(moves[1])
                surf, rect = render_text(txt, (panel_x + scale(130), row_y), size=int(scale(20)), color=(200, 200, 200), draw=False)
                
                # Interaction
                if rect.collidepoint(mouse_pos):
                    pygame.draw.rect(self.screen, (70, 70, 70), rect, border_radius=3)
                    if mouse_click:
                        self.rollback(int(move_idx), 1)
                        self.screen.set_clip(None)
                        return

                self.screen.blit(surf, rect)

        # Reset clip so other UI elements draw normally
        self.screen.set_clip(None)

        # 4. Draw Top and Bottom "Fade" or Border Rects
        # These hide the text as it scrolls "under" the header/footer
        pygame.draw.rect(self.screen, (60, 60, 60), full_rect, width=2, border_radius=5)

    def init_pieces_from_board(self):
        # Re-uses logic from __init__ to rebuild piece objects from self.board
        for row in range(8):
            lane: list[Pieces.Piece | None] = []
            for col in range(8):
                piece_symbol = self.board[row][col]
                piece: Pieces.Piece | None = None
                if piece_symbol is not None:
                    color = Pieces.PieceColor.WHITE if piece_symbol.isupper() else Pieces.PieceColor.BLACK
                    symbol = piece_symbol.upper()
                    for pt in Pieces.PieceType.__dict__.values():
                        if isinstance(pt, dict) and pt["symbol"] == symbol:
                            piece = Pieces.Piece(pt, color)
                            piece.set_position(col, row)
                            # Note: Castling rights on Piece objects are updated in update_board loop
                            # based on position, but we rely on Engine for logic.
                            break
                lane.append(piece)
            self.pieces.append(lane)

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    app = App()
    app.run()
