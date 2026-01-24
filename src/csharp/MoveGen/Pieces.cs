using System;
using System.Collections.Generic;
using System.Linq;

namespace pieces
{
	public class Moves
	{

        public List<Tuple<int, int>> King_Dir = new List<Tuple<int, int>>
        {
            Tuple.Create(0, 1),   // North
            Tuple.Create(0, -1),  // South
            Tuple.Create(1, 0),   // East
            Tuple.Create(-1, 0),  // West
            Tuple.Create(1, 1),   // North-East
            Tuple.Create(1, -1),  // South-East
            Tuple.Create(-1, 1),  // North-West
            Tuple.Create(-1, -1)  // South-West
        };

        public List<Tuple<int, int>> Queen_Dir = new List<Tuple<int, int>>
        {
            Tuple.Create(0, 1),   // North
            Tuple.Create(0, -1),  // South
            Tuple.Create(1, 0),   // East
            Tuple.Create(-1, 0),  // West
            Tuple.Create(1, 1),   // North-East
            Tuple.Create(1, -1),  // South-East
            Tuple.Create(-1, 1),  // North-West
            Tuple.Create(-1, -1)  // South-West
        };

        public List<Tuple<int, int>> Rook_Dir = new List<Tuple<int, int>>
        {
            Tuple.Create(0, 1),   // North
            Tuple.Create(0, -1),  // South
            Tuple.Create(1, 0),   // East
            Tuple.Create(-1, 0)  // West
        };

        public List<Tuple<int, int>> Bishop_Dir = new List<Tuple<int, int>>
        {
            Tuple.Create(1, 1),   // North-East
            Tuple.Create(1, -1),  // South-East
            Tuple.Create(-1, 1),  // North-West
            Tuple.Create(-1, -1)  // South-West
        };

        public List<Tuple<int, int>> Knight_Dir = new List<Tuple<int, int>>
        {
            Tuple.Create(1, 2),   // North-East
            Tuple.Create(1, -2),  // South-East
            Tuple.Create(-1, 2),  // North-West
            Tuple.Create(-1, -2),  // South-West
            Tuple.Create(2, 1), // East-North
            Tuple.Create(2, -1), // East-South
            Tuple.Create(-2, 1), // West-North
            Tuple.Create(-2, -1), // West-South
        };

        public List<Tuple<int, int>> Pawn_Dir = new List<Tuple<int, int>>
        {
            Tuple.Create(0, 1),   // North
            Tuple.Create(1,1),  // North - East
            Tuple.Create(-1, 1), // North - West
        };

        public List<Tuple<int,int>> Get_Dir(string piece)
        {
            return piece.ToLower() switch
            {
                "k" => King_Dir,
                "q" => Queen_Dir,
                "r" => Rook_Dir,
                "b" => Bishop_Dir,
                "n" => Knight_Dir,
                "p" => Pawn_Dir,
                _ => new List<Tuple<int, int>>(),
            };
        }

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

                case "p":
                    foreach (var dir in Pawn_Dir)
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
                    throw new Exception("Not a valid piece");
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