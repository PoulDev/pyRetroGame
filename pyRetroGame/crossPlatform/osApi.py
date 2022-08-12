import os
import msvcrt
from ..mathematics.vector import Vector2

"""
    Sadly for now, this project is not cross-platform.
    why? because the library msvcrt is not supported on linux, and we didn't
    find any cross-platform solution.

    if you have any idea / suggestion to make this project cross-platform,
    please open a issue on github.
"""

clearCommand = 'cls' if os.name == 'nt' else 'clear'

def waitKey(stdscr = None) -> int:
    keyPressed = msvcrt.kbhit()
    return ord(msvcrt.getch()) if keyPressed else 0

def terminalSize() -> Vector2:
    size = os.get_terminal_size()
    return Vector2(size.columns, size.lines)
