# Chess

A hybrid **Python + C# chess engine** with a library for playing chess, move generation, and AI integration via Python scripts.

## Features

* **Fast C# Chess Engine**: Efficient move generation and evaluation.
* **Python Integration**: Interact with the engine through `translate.py`.
* **Automated Build Workflow**: `dotnet watch` rebuilds the DLL on C# code changes.
* **AI-ready Architecture**: Easily integrate evaluation functions, heuristics, or AI logic.
* **Testing Utilities**: Python scripts for quick engine testing and validation.

## Project Structure

```
Chess/
├── src/
│   ├── python/
│   │   └── translate.py        # Python script to load and test the C# engine
│   └── csharp/
│       └── MoveGen/
│           ├── Engine.cs       # C# engine code
│           ├── MoveGen.csproj  # C# project
│           └── bin/Debug/net9.0/MoveGen.dll
├── assets/                      # (Optional) images, icons, etc.
├── README.md
```

## Requirements

* Python 3.9–3.13
* .NET SDK 9 or 10
* `pythonnet` library

```bash
pip install pythonnet
```

## Installation & Quick Start

1. Clone the repository:

```bash
git clone https://github.com/Rudravns/Chess.git
cd Chess
```

2. Build the C# DLL (VS Code Insiders terminal):

```powershell
cd src/csharp/MoveGen
dotnet watch build
```

This rebuilds the DLL automatically whenever you save C# files.

3. Run Python integration (regular VS Code terminal):

```powershell
python src/python/translate.py
```

Expected output:

```
C# assembly loaded successfully.
C# Engine instantiated successfully!
C# engine loaded successfully
2 + 3 = 5
```

## Workflow

1. Edit **C# engine** → Save → DLL rebuilds automatically.
2. Run Python scripts → Load the updated engine.
3. Optional: Use a Python watcher script to reload the engine automatically when DLL changes.

## Example Usage

```python
from translate import load_engine, test_engine

engine = load_engine()
test_engine(engine)

# Later, integrate actual chess moves:
# moves = engine.GenerateMoves(fen)
# engine.MakeMove(move)
```

## Contributing

* Add features to `MoveGen/Engine.cs` for move generation, AI, or evaluation.
* Add Python scripts in `src/python` for testing or AI logic.
* Always rebuild DLL after C# changes (`dotnet build` or watch mode).

## License

MIT License

## Author

Rudransh (Rudravns)
