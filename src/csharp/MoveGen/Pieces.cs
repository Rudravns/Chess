using System;
using System.Collections.Generic;

namespace pieces
{
    public class Moves
    {
        public List<Tuple<int, int>> King_Dir = new()
        {
            Tuple.Create(0, 1),
            Tuple.Create(0, -1),
            Tuple.Create(1, 0),
            Tuple.Create(-1, 0),
            Tuple.Create(1, 1),
            Tuple.Create(1, -1),
            Tuple.Create(-1, 1),
            Tuple.Create(-1, -1)
        };

        public List<Tuple<int, int>> Queen_Dir = new()
        {
            Tuple.Create(0, 1),
            Tuple.Create(0, -1),
            Tuple.Create(1, 0),
            Tuple.Create(-1, 0),
            Tuple.Create(1, 1),
            Tuple.Create(1, -1),
            Tuple.Create(-1, 1),
            Tuple.Create(-1, -1)
        };

        public List<Tuple<int, int>> Rook_Dir = new()
        {
            Tuple.Create(0, 1),
            Tuple.Create(0, -1),
            Tuple.Create(1, 0),
            Tuple.Create(-1, 0)
        };

        public List<Tuple<int, int>> Bishop_Dir = new()
        {
            Tuple.Create(1, 1),
            Tuple.Create(1, -1),
            Tuple.Create(-1, 1),
            Tuple.Create(-1, -1)
        };

        public List<Tuple<int, int>> Knight_Dir = new()
        {
            Tuple.Create(1, 2),
            Tuple.Create(1, -2),
            Tuple.Create(-1, 2),
            Tuple.Create(-1, -2),
            Tuple.Create(2, 1),
            Tuple.Create(2, -1),
            Tuple.Create(-2, 1),
            Tuple.Create(-2, -1)
        };

        // 🔹 NO PAWNS HERE 🔹

        public List<Tuple<int, int>> All_Moves(string piece, int col, int row)
        {
            List<Tuple<int, int>> allMoves = new();

            switch (piece.ToLower())
            {
                case "k":
                    foreach (var dir in King_Dir)
                        allMoves.Add(Tuple.Create(col + dir.Item1, row + dir.Item2));
                    break;

                case "n":
                    foreach (var dir in Knight_Dir)
                        allMoves.Add(Tuple.Create(col + dir.Item1, row + dir.Item2));
                    break;

                case "q":
                    foreach (var dir in Queen_Dir)
                        allMoves.AddRange(SlidingMoves(dir, col, row));
                    break;

                case "r":
                    foreach (var dir in Rook_Dir)
                        allMoves.AddRange(SlidingMoves(dir, col, row));
                    break;

                case "b":
                    foreach (var dir in Bishop_Dir)
                        allMoves.AddRange(SlidingMoves(dir, col, row));
                    break;

                default:
                    throw new Exception($"Invalid piece type: {piece}");
            }

            return allMoves;
        }

        private List<Tuple<int, int>> SlidingMoves(Tuple<int, int> dir, int col, int row)
        {
            List<Tuple<int, int>> moves = new();

            int x = col + dir.Item1;
            int y = row + dir.Item2;

            while (x >= 0 && x < 8 && y >= 0 && y < 8)
            {
                moves.Add(Tuple.Create(x, y));
                x += dir.Item1;
                y += dir.Item2;
            }

            return moves;
        }
    }
}
