#!/usr/bin/env python3
import os
import sys

if __name__ == "__main__":
    if os.uname()[4].startswith('arm'):
        if sys.argv[1] == 'tft':
            from showtime.raspberrytft import showtime
        else:
            from showtime.raspberrypi import showtime
    else:
        from showtime.desktop import showtime
    showtime()
