# Chess

A hybrid **Python + C# chess engine** application. The user interface and game loop are built with Python (Pygame), while the heavy lifting of move generation and validation is handled by a high-performance C# library loaded via Python.NET.

## Features

*   **Interactive GUI**: Play chess with a drag-and-drop interface.
*   **Hybrid Architecture**: Python frontend for ease of development, C# backend for speed.
*   **Move Validation**: Legal moves, checks, and pins are calculated by the C# engine.
*   **Special Moves**: Full support for Castling, En Passant, and Pawn Promotion.
*   **Move History (PGN)**:
    *   Automatic PGN generation.
    *   Scrollable move history panel.
    *   **Time Travel**: Click on any previous move in the history to revert the game state to that point.
*   **FEN Support**: Game state is tracked via FEN strings; supports loading/saving.

## Prerequisites

*   **Python 3.x**
*   **.NET 9.0 SDK** (Required to build the C# backend)
*   **Python Packages**:
    *   `pygame`
    *   `pythonnet`
    *   `numpy`

## Installation & Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd Chess
    ```

2.  **Build the C# Backend**:
    Navigate to the C# project directory and build it. This generates the `MoveGen.dll` required by the Python script.
    ```bash
    cd src/csharp/MoveGen
    dotnet build
    ```
    *Ensure the build output is located at `src/csharp/MoveGen/bin/Debug/net9.0/MoveGen.dll` as expected by the Python script.*

3.  **Install Python Dependencies**:
    ```bash
    pip install pygame pythonnet numpy
    ```

4.  **Run the Game**:
    Navigate to the Python source directory and run the main script.
    ```bash
    cd src/python
    python Main.py
    ```

## File Structure

```text
Chess/
├── assets/                 # Images and sound resources
├── data/                   # Configuration files (settings.json)
├── games/                  # Saved game files (.json)
├── src/
│   ├── csharp/
│   │   └── MoveGen/        # C# Backend Project
│   │       ├── Main.cs     # Engine logic entry point
│   │       ├── Possible_moves.cs # Move generation logic
│   │       ├── Pieces.cs   # Piece definitions and movement directions
│   │       ├── Helper.cs   # FEN string parsing
│   │       ├── MoveGen.csproj # Project definition
│   │       └── bin/        # Build output (DLLs)
│   └── python/
│       ├── Main.py         # Application entry point
│       ├── Helper.py       # Utility functions (rendering, file I/O)
│       ├── Translate.py    # Python.NET bridge to C# DLL
│       ├── Pieces.py       # Piece definitions
│       ├── Notation.py     # FEN and algebraic notation logic
│       ├── Watcher.py      # Automatically build C# DLL on change
│       ├── base_data.py    # Base data definitions
│       └── Data_types.py   # Constants and type definitions
├── Chess.sln               # Project configuration
├── .gitignore 
└── README.md
```
