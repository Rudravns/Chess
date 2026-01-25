using System;

public static class FenParser
{
    public static List<List<string?>> Parse(string fen)
    {
        var board = new List<List<string?>>();
        var rows = fen.Split(' ')[0].Split('/');

        foreach (var row in rows)
        {
            var boardRow = new List<string?>();
            foreach (char c in row)
            {
                if (char.IsDigit(c))
                {
                    for (int i = 0; i < c - '0'; i++)
                        boardRow.Add(null);
                }
                else
                {
                    boardRow.Add(c.ToString());
                }
            }
            board.Add(boardRow);
        }

        return board;
    }

}


