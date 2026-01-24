using System.Collections.Generic;
using Possible_moves;

namespace MoveGen
{
    public class Engine
    {
        private List<List<string?>> board;
        private Possible_move moveGen;

        public Engine()
        {
            board = new List<List<string?>>();
            moveGen = new Possible_move(this);
        }

        public void SetBoardFromFEN(string fen)
        {
            board = FenParser.Parse(fen);
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
