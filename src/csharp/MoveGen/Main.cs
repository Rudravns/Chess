using System.Collections.Generic;
using Possible_moves;

namespace MoveGen
{
    public class Engine
    {
        private List<List<string?>> board;
        private Possible_move moveGen;

        // Track castling rights
        public bool WhiteCanCastleKingside { get; private set; } = true;
        public bool WhiteCanCastleQueenside { get; private set; } = true;
        public bool BlackCanCastleKingside { get; private set; } = true;
        public bool BlackCanCastleQueenside { get; private set; } = true;

        public Engine()
        {
            board = new List<List<string?>>();
            moveGen = new Possible_move(this);
        }

        // Example getters used in Possible_move
        public bool CanCastleKingSide(bool isWhite)
        {
            return isWhite ? WhiteCanCastleKingside : BlackCanCastleKingside;
        }

        public bool CanCastleQueenSide(bool isWhite)
        {
            return isWhite ? WhiteCanCastleQueenside : BlackCanCastleQueenside;
        }

        // Call this whenever king or rook moves to disable castling
        public void DisableCastling(bool isWhite, bool kingside)
        {
            if (isWhite)
            {
                if (kingside) WhiteCanCastleKingside = false;
                else WhiteCanCastleQueenside = false;
            }
            else
            {
                if (kingside) BlackCanCastleKingside = false;
                else BlackCanCastleQueenside = false;
            }
        }

        public Tuple<int, int>? EnPassantSquare { get; private set; }

        public void SetBoardFromFEN(string fen)
        {
            var parts = fen.Split(' ');

            board = FenParser.Parse(fen); 

            // en passant
            if (parts[3] != "-")
            {
                int file = parts[3][0] - 'a';
                int rank = 8 - (parts[3][1] - '0');
                EnPassantSquare = Tuple.Create(file, rank);
            }
            else
            {
                EnPassantSquare = null;
            }
        }


       

        public ref List<List<string?>> GetBoard()
        {
            return ref board;
        }

        public List<(int col, int row)> GetLegalMoves(int col, int row)
        {
            return moveGen.Legal_moves(col, row)
                         .Select(t => (t.Item1, t.Item2))
                         .ToList();
        }

        // testing
        public string Hello() => "C# engine loaded successfully";
        public int Add(int a, int b) => a + b;
    }
}
