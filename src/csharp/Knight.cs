using System;
using System.Collections.Generic;

namespace MoveGen
{
    public static class Knight
    {
        public static List<string> GetMoves(int rank, int file)
        {
            List<string> moves = new List<string>();
            // Knight offsets: the 8 "L" shapes
            int[] dRank = { 2, 1, -1, -2, -2, -1, 1, 2 };
            int[] dFile = { 1, 2, 2, 1, -1, -2, -2, -1 };

            for (int i = 0; i < 8; i++)
            {
                int nextR = rank + dRank[i];
                int nextF = file + dFile[i];

                if (nextR >= 0 && nextR < 8 && nextF >= 0 && nextF < 8)
                {
                    moves.Add($"Square: {nextR},{nextF}");
                }
            }
            return moves;
        }
    }
}
