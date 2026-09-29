"""Read single key presses in Windows and Unix-like terminals."""

import os
import sys

if os.name == "nt":
    import msvcrt

    def key_pressed():
        return msvcrt.kbhit()

    def read_key():
        return msvcrt.getwch().lower()
else:
    import select
    import termios
    import tty

    def key_pressed():
        ready, _, _ = select.select([sys.stdin], [], [], 0)
        return bool(ready)

    def read_key():
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setcbreak(sys.stdin.fileno())
            return sys.stdin.read(1).lower()
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
