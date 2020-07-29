#!/usr/bin/env python3
import os

if __name__ == "__main__":
    if os.uname()[4].startswith('arm'):
        from showtime.raspberrypi import showtime
    else:
        from showtime.desktop import showtime
    showtime()
