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

        public List<Tuple<int, int>> Legal_moves(int col, int row)
        {
            ref List<List<string?>> board = ref engine.GetBoard();

            List<Tuple<int, int>> legalMoves = new();

            string? piece = board[row][col];
            if (piece == null)
                return legalMoves;

            bool isWhite = char.IsUpper(piece[0]);
            string pieceType = piece[^1].ToString(); // last char: p, r, n, b, q, k

            var pseudoMoves = Dirs.All_Moves(pieceType, col, row);

            foreach (var move in pseudoMoves)
            {
                int x = move.Item1;
                int y = move.Item2;

                // 1 board bounds
                if (x < 0 || x >= 8 || y < 0 || y >= 8)
                    continue;

                string? target = board[y][x];

                // 2 empty square -> OK
                if (target == null)
                {
                    legalMoves.Add(move);
                    continue;
                }

                // 3 capture enemy only
                bool targetIsWhite = char.IsUpper(target[0]);

                if (isWhite != targetIsWhite)
                {
                    legalMoves.Add(move);
                }
            }

            return legalMoves;
        }



    }
}
