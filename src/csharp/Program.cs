using System;
using System.Collections.Generic;

namespace MoveGen
{
    public class Engine
    {
        // This is the "Front Desk" that Python talks to
        public static string[] GetLegalMoves(string fen)
        {
            // For now, let's pretend we parsed the FEN 
            // and found a Knight on d4 (Rank 4, File 3)

            // We call the Specialist (Knight.cs) to do the math
            List<string> moves = Knight.GetMoves(4, 3);

            // Convert back to an array to send to Python
            return moves.ToArray();
        }

        // Necessary to keep the compiler happy for a Console project
        public static void Main(string[] args)
        {
            Console.WriteLine("Chess Engine DLL Loaded.");
        }
    }
}
