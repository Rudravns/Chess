# watcher.py
import time
import os
from Translate import load_engine, test_engine

DLL_PATH = os.path.abspath("../../csharp/MoveGen/bin/Debug/net9.0/MoveGen.dll")
last_mtime = 0

while True:
    if os.path.exists(DLL_PATH):
        mtime = os.path.getmtime(DLL_PATH)
        if mtime != last_mtime:
            print("DLL changed, reloading engine...")
            engine = load_engine()
            test_engine(engine)
            last_mtime = mtime
    time.sleep(1)
