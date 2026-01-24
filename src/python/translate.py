import os
import sys
from pythonnet import load

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
        print("C# assembly loaded successfully.")
    except Exception as e:
        raise RuntimeError(f"Failed to load C# assembly: {e}")

    try:
        from MoveGen import Engine # pyright: ignore[reportMissingImports]
        engine = Engine()
        print("C# Engine instantiated successfully!")
        return engine
    except Exception as e:
        raise ImportError(
            "Failed to import Engine from MoveGen. "
            "Check namespace and class name in C# code."
        ) from e

def test_engine(engine):
    """Run simple tests to verify integration."""
    print(engine.Hello())
    print("2 + 3 =", engine.Add(2, 3))

# --------------------------------------------------
# Entry point
# --------------------------------------------------
if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    engine = load_engine()
    test_engine(engine)
