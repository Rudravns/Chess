using System;
using System.Collections.Generic;
using MoveGen;
using pieces;
using System.Linq;
using System.Diagnostics;

namespace Possible_moves
{
    public class Possible_move
    {
        private readonly Engine engine;
        private readonly Moves dirs = new Moves();
        public Moves Dirs = new Moves();

        public Possible_move(Engine engine)
        {
            this.engine = engine;
        }

        //  Returns whether a square is under attack by enemy pieces
        public bool SquareUnderAttack(int col, int row, bool friendlyIsWhite)
        {
            var board = engine.GetBoard();
            for (int r = 0; r < 8; r++)
            {
                for (int c = 0; c < 8; c++)
                {
                    var piece = board[r][c];
                    if (piece == null) continue;

                    bool pieceIsWhite = char.IsUpper(piece[0]);
                    if (pieceIsWhite == friendlyIsWhite) continue;

                    // Get pseudo-legal moves for enemy piece
                    var moves = LegalMovesPseudo(c, r);
                    foreach (var m in moves)
                    {
                        if (m.Item1 == col && m.Item2 == row)
                            return true;
                    }
                }
            }
            return false;
        }

        //  Get pseudo-legal moves ignoring king safety
        private List<Tuple<int, int>> LegalMovesPseudo(int col, int row)
        {
            var board = engine.GetBoard();
            List<Tuple<int, int>> moves = new();
            string? piece = board[row][col];
            if (piece == null) return moves;

            bool isWhite = char.IsUpper(piece[0]);
            string pieceType = piece.ToLower();

            if (pieceType == "p")
            {
                AddPawnMoves(moves, col, row, isWhite, board);
                return moves;
            }

            if (pieceType == "r")
            {
                AddSlidingMoves(moves, dirs.Rook_Dir, col, row, isWhite, board);
                return moves;
            }

            if (pieceType == "b")
            {
                AddSlidingMoves(moves, dirs.Bishop_Dir, col, row, isWhite, board);
                return moves;
            }

            if (pieceType == "q")
            {
                AddSlidingMoves(moves, dirs.Queen_Dir, col, row, isWhite, board);
                return moves;
            }

            // King/knight pseudo-moves
            moves.AddRange(dirs.All_Moves(pieceType, col, row).Where(m =>
            {
                int x = m.Item1;
                int y = m.Item2;
                if (!InBounds(x, y)) return false;

                string? target = board[y][x];
                return target == null || char.IsUpper(target[0]) != isWhite;
            }));

            return moves;
        }

        //  Returns fully legal moves (filter out moves leaving king in check)
        public List<Tuple<int, int>> Legal_moves(int col, int row)
        {
            var board = engine.GetBoard();
            List<Tuple<int, int>> legalMoves = new();
            if (!InBounds(col, row)) return legalMoves;

            string? piece = board[row][col];
            if (piece == null) return legalMoves;

            bool isWhite = char.IsUpper(piece[0]);
            string pieceType = piece.ToLower();

            // Generate pseudo-legal moves
            List<Tuple<int, int>> pseudoMoves = LegalMovesPseudo(col, row);

            foreach (var move in pseudoMoves)
            {
                int newCol = move.Item1;
                int newRow = move.Item2;

                // simulate move
                string? originalTarget = board[newRow][newCol];
                board[newRow][newCol] = piece;
                board[row][col] = null;

                bool kingSafe = true;

                // Find king position
                Tuple<int, int> kingPos = pieceType == "k" ? Tuple.Create(newCol, newRow) : FindKingPosition(isWhite, board);

                // Check if king is attacked
                if (SquareUnderAttack(kingPos.Item1, kingPos.Item2, isWhite))
                    kingSafe = false;

                // revert move
                board[row][col] = piece;
                board[newRow][newCol] = originalTarget;

                if (kingSafe)
                    legalMoves.Add(move);
            }

            //  Add castling moves if king
            if (pieceType == "k")
            {
                legalMoves.AddRange(GetCastlingMoves(col, row, isWhite, board));
            }

            return legalMoves;
        }

        //  Find king position
        private Tuple<int, int> FindKingPosition(bool isWhite, List<List<string?>> board)
        {
            for (int r = 0; r < 8; r++)
                for (int c = 0; c < 8; c++)
                    if (board[r][c]?.ToLower() == "k" && (char.IsUpper(board[r][c][0]) == isWhite))
                        return Tuple.Create(c, r);
            throw new Exception("King not found!");
        }

        //  Generate legal castling moves
        private List<Tuple<int, int>> GetCastlingMoves(int col, int row, bool isWhite, List<List<string?>> board)
        {
            List<Tuple<int, int>> moves = new();

            // Kingside
            if (engine.CanCastleKingSide(isWhite))
            {
                if (board[row][col + 1] == null && board[row][col + 2] == null &&
                    !SquareUnderAttack(col, row, isWhite) &&
                    !SquareUnderAttack(col + 1, row, isWhite) &&
                    !SquareUnderAttack(col + 2, row, isWhite))
                {
                    moves.Add(Tuple.Create(col + 2, row));
                }
            }

            // Queenside
            if (engine.CanCastleQueenSide(isWhite))
            {
                if (board[row][col - 1] == null && board[row][col - 2] == null && board[row][col - 3] == null &&
                    !SquareUnderAttack(col, row, isWhite) &&
                    !SquareUnderAttack(col - 1, row, isWhite) &&
                    !SquareUnderAttack(col - 2, row, isWhite))
                {
                    moves.Add(Tuple.Create(col - 2, row));
                }
            }

            return moves;
        }

        //  Sliding pieces helper
        private void AddSlidingMoves(
            List<Tuple<int, int>> moves,
            List<Tuple<int, int>> directions,
            int col,
            int row,
            bool isWhite,
            List<List<string?>> board
        )
        {
            foreach (var dir in directions)
            {
                int x = col + dir.Item1;
                int y = row + dir.Item2;

                while (InBounds(x, y))
                {
                    string? target = board[y][x];
                    if (target == null)
                        moves.Add(Tuple.Create(x, y));
                    else
                    {
                        if (char.IsUpper(target[0]) != isWhite)
                            moves.Add(Tuple.Create(x, y));
                        break;
                    }
                    x += dir.Item1;
                    y += dir.Item2;
                }
            }
        }

        //  Pawn moves helper
        // Inside Possible_move.cs -> AddPawnMoves method
        private void AddPawnMoves(List<Tuple<int, int>> moves, int col, int row, bool isWhite, List<List<string?>> board)
        {
            int dir = isWhite ? -1 : 1;
            int startRow = isWhite ? 6 : 1;

            // 1. Forward Move
            int oneStepRow = row + dir;
            if (InBounds(col, oneStepRow) && board[oneStepRow][col] == null)
            {
                moves.Add(Tuple.Create(col, oneStepRow));
                // 2. Double Step
                int twoStepRow = row + dir * 2;
                if (row == startRow && board[twoStepRow][col] == null)
                    moves.Add(Tuple.Create(col, twoStepRow));
            }

            // 3. Diagonal Captures
            foreach (int dx in new[] { -1, 1 })
            {
                int x = col + dx;
                int y = row + dir;
                if (!InBounds(x, y)) continue;

                string? target = board[y][x];
                // Standard capture
                if (target != null && char.IsUpper(target[0]) != isWhite)
                    moves.Add(Tuple.Create(x, y));

                // 4. EN PASSANT LOGIC
                var ep = engine.EnPassantSquare;
                if (ep != null && ep.Item1 == x && ep.Item2 == y)
                {
                    moves.Add(Tuple.Create(x, y));
                }
            }
        }

        private bool InBounds(int x, int y)
        {
            return x >= 0 && x < 8 && y >= 0 && y < 8;
        }
    }
}
