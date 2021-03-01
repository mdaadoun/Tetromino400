import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup (
    name = "Tetromino400",
    version = "1.0",
    description = "A famous falling blocks game clone.",
    options = {"build_exe":build_exe_options},
    executables = [Executable("game.py", base=base)]
)
