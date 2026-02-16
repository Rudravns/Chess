import os
import sys
from pythonnet import load
import Notation
import Data_types

debug = False


def setup_dotnet_runtime():
    """Load the .NET Core runtime before using clr."""
    load("coreclr")
    import clr
    return clr

def get_dll_path():
    """Resolve the path to MoveGen.dll."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dll_dir = os.path.abspath(
        os.path.join(script_dir, "..", "csharp", "MoveGen", "bin", "Debug", "net9.0")
    )
    dll_path = os.path.join(dll_dir, "MoveGen.dll")

    if not os.path.exists(dll_path):
        raise FileNotFoundError(
            f"MoveGen.dll not found at:\n{dll_path}\n"
            "Build the C# project first."
        )

    # Add DLL folder to Python path
    if dll_dir not in sys.path:
        sys.path.append(dll_dir)

    return dll_path

def load_engine():
    """Load the C# assembly and return an instance of Engine."""
    clr = setup_dotnet_runtime()
    dll_path = get_dll_path()

    try:
        clr.AddReference("MoveGen") # pyright: ignore[reportAttributeAccessIssue]
        if debug: print("C# assembly loaded successfully.")
    except Exception as e:
        raise RuntimeError(f"Failed to load C# assembly: {e}")

    try:
        from MoveGen import Engine # pyright: ignore[reportMissingImports]
        engine = Engine()
        if debug: print("C# Engine instantiated successfully!")
        return engine
    except Exception as e:
        raise ImportError(
            "Failed to import Engine from MoveGen. "
            "Check namespace and class name in C# code."
        ) from e

def test_engine(engine):
    """Run simple tests to verify integration."""
    if debug: print(engine.Hello())
    if debug: print("2 + 3 =", engine.Add(2, 3))

engine = load_engine()
engine.SetBoardFromFEN(Data_types.START_FEN)

# --------------------------------------------------
# Entry point
# --------------------------------------------------
if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    test_engine(engine)
    if debug: print("\n\n")
    engine.SetBoardFromFEN(Data_types.START_FEN)
    

    moves = engine.GetLegalMoves(0, 1)
    py_moves = [(m.Item1, m.Item2) for m in moves]
    if debug: print(py_moves)