#!/usr/bin/env python3

# standard library
import time
import os
import json
from datetime import datetime

#  display drivers
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7735 as st7735

#  my utility libraries
from .trains_util import get_trains
from .weather_util import get_weather
from .tides_util import get_tides


def get_time():
    return datetime.now().strftime('%H:%M%')


def get_date():
    return datetime.now().strftime('%d-%m%-%Y')


def get_datetime():
    return '  '.join(get_time(), get_date())


def format_tides():
    tides = get_tides()
    m = ' Moon: {}%, {}'.format(tides['moon']['pct'], tides['moon']['phase'])
    td = ["{}{}".format(item.get('desc').replace('high', chr(0x18)).replace('low', chr(0x19)), item.get('ts'))
          for item in tides['tides']]
    t = ' Tides @ {}: {}'.format(tides['location'], ", ".join(td))
    return "{} {}".format(m, t)


def read_sensor_data():
    """
    Read Temperature and Humidity Sensor data and display.
    Prologue-TH wireless outdoor sensor is being used.
    rtl_433 utility will read the data via radio data channel
    and save the output to the file as a series of json objects.
    The command is scheduled in Cron:
    > rtl_433 -f 433920000 -R 03 -E quit -F json
    """
    filename = '/home/pi/pizero-clock/prologue/prologue.json'
    degree_sign = chr(248)
    if os.path.exists(filename):
        with open(filename) as f:
            data = f.readlines()[-1]
            if data:
                th = json.loads(data)
                return " Out: {}{}C @ {}%".format(th.get('temperature_C'),
                                                    degree_sign,
                                                    th.get('humidity'))
    else:
        return ''


def showtime():
    #  setup display
    # Configuration for CS and DC pins (these are PiTFT defaults):
    cs_pin = digitalio.DigitalInOut(board.CE0)
    dc_pin = digitalio.DigitalInOut(board.D25)
    reset_pin = digitalio.DigitalInOut(board.D24)

    # Config for display baudrate (default max is 24mhz):
    BAUDRATE = 24000000

    # Setup SPI bus using hardware SPI:
    spi = board.SPI()

    # Create the display:
    disp = st7735.ST7735S(spi,
                          rotation=90,
                          cs=cs_pin,
                          dc=dc_pin,
                          rst=reset_pin,
                          baudrate=BAUDRATE)

    # Create blank image for drawing.
    # Make sure to create image with mode 'RGB' for full color.
    if disp.rotation % 180 == 90:
        height = disp.width  # we swap height/width to rotate it to landscape!
        width = disp.height
    else:
        width = disp.width  # we swap height/width to rotate it to landscape!
        height = disp.height

    image = Image.new("RGB", (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    disp.image(image)

    # First define some constants to allow easy positioning of text.
    padding = -2
    x = 0

    # Load a TTF font.  Make sure the .ttf font file is in the
    # same directory as the python script!
    # Some other nice fonts to try: http://www.dafont.com/bitmap.php
    font = ImageFont.truetype("/usr/share/fonts/truetype/msttcorefonts/Impact.ttf", 16)

    # between 6 and 10 show trains
    trains = ''
    present = datetime.now()
    if (present.hour >= 6 and present.hour <= 10):
        #  show next three trains
        train_times = [tm.strftime('%H:%M') for tm in get_trains()[:3]]
        trains = ', '.join(train_times)

    weather = get_weather()
    out_T = read_sensor_data()
    tides = format_tides()
    dt = get_datetime()

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Shell scripts for system monitoring from here:
    # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d' ' -f1"
    IP = "IP: " + subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%d GB  %s", $3,$2,$5}\''
    Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "cat /sys/class/thermal/thermal_zone0/temp |  awk '{printf \"CPU t: %.1f C\", $(NF-0) / 1000}'"  # pylint: disable=line-too-long
    Temp = subprocess.check_output(cmd, shell=True).decode("utf-8")

    # Write four lines of text.
    y = padding
    draw.text((x, y), IP, font=font, fill="#FFFFFF")
    y += font.getsize(IP)[1]
    draw.text((x, y), CPU, font=font, fill="#FFFF00")
    y += font.getsize(CPU)[1]
    draw.text((x, y), MemUsage, font=font, fill="#00FF00")
    y += font.getsize(MemUsage)[1]
    draw.text((x, y), Disk, font=font, fill="#0000FF")
    y += font.getsize(Disk)[1]
    draw.text((x, y), Temp, font=font, fill="#FF00FF")

    y += font.getsize(trains)[1]
    draw.text((x, y), trains, font=font, fill="#FF00FF")
    y += font.getsize(weather)[1]
    draw.text((x, y), weather, font=font, fill="#FF00FF")
    y += font.getsize(out_T)[1]
    draw.text((x, y), out_T, font=font, fill="#FF00FF")
    y += font.getsize(tides)[1]
    draw.text((x, y), tides, font=font, fill="#FF00FF")
    y += font.getsize(dt)[1]
    draw.text((x, y), dt, font=font, fill="#FF00FF")
    # Display image.
    disp.image(image)
