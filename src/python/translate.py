import sys
import os
import clr # type: ignore
from pythonnet import load # type: ignore

# 1. Start the .NET Runtime
try:
    load("coreclr")
except:
    pass

# 2. Get the ABSOLUTE path to your DLL folder
# This goes up from 'src/python' to the 'Chess' root, then into 'bin'
base_dir = os.path.dirname(os.path.abspath(__file__))
dll_dir = os.path.join(base_dir, "..", "..", "bin", "Debug", "net9.0")

# 3. Add to sys.path so Python can see the 'MoveGen' module
if dll_dir not in sys.path:
    sys.path.append(dll_dir)

# 4. Load the DLL
try:
    clr.AddReference("Chess") # type: ignore
    import MoveGen # type: ignore
    from MoveGen import Engine # type: ignore
    print("✅ Success! Bridge is working.")
    print("Moves:", list(Engine.GetLegalMoves("startpos")))
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"Checked path: {os.path.abspath(dll_dir)}")
