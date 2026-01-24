Chess

A hybrid Python + C# chess engine with a basic library for playing chess, move generation, and testing AI logic.

Features

C# backend for fast chess move generation and evaluation

Python frontend for running scripts and integrating AI

Easy-to-use engine API via translate.py

Fully automated workflow with hot-reload support (DLL rebuilds automatically on C# code changes)

Folder Structure

Chess/
├─ src/
│  ├─ python/
│  │  └─ translate.py      # Python script to load C# engine
│  └─ csharp/
│     └─ MoveGen/
│        ├─ Engine.cs      # C# engine code
│        ├─ MoveGen.csproj # C# project
│        └─ bin/Debug/net9.0/MoveGen.dll
├─ assets/                  # (Optional) images, icons, etc.
├─ README.md

Getting Started

Requirements

Python 3.9–3.13

.NET SDK 9 or 10

pythonnet library

pip install pythonnet

Setup

Build the C# DLL (run this in VS Code Insiders terminal inside src/csharp/MoveGen):

dotnet watch build

Run the Python integration (in regular VS Code terminal):

python src/python/translate.py

You should see:

C# assembly loaded successfully.
C# Engine instantiated successfully!
C# engine loaded successfully
2 + 3 = 5

Workflow

Edit C# engine → Save → DLL rebuilds automatically (dotnet watch build)

Run Python scripts → Load the updated engine instantly

Optional: Use watcher.py (Python script) to auto-reload engine when DLL changes

Example Usage

from translate import load_engine, test_engine

engine = load_engine()
test_engine(engine)

# Later, replace test_engine() with actual chess moves:
# moves = engine.GenerateMoves(fen)
# engine.MakeMove(move)

Contributing

Add new features to C# engine in MoveGen/Engine.cs

Add Python scripts or AI logic in src/python

Always rebuild DLL after changes (dotnet build or watch mode)

License

MIT License

