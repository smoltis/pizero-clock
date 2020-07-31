#!/usr/bin/env python3

# standard library
import time
import os
import json
from datetime import datetime

#  display drivers
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT

#  my utility libraries
from .trains_util import get_trains
from .weather_util import get_weather
from .tides_util import get_tides

# TODO: Add tides
# TODO: add outdoor temperature sensor
# TODO: add speaker
# TODO: add webUI


def animation_dt(device, from_y, to_y, dt):
    #  Animate the whole thing, moving it into/out of the abyss.
    hours_time = dt.strftime('%H')
    min_time = dt.strftime('%M')
    current_y = from_y
    while current_y != to_y:
        with canvas(device) as draw:
            text(draw, (0, 0), "l", fill="white", font=proportional(TINY_FONT))
            text(draw, (1, current_y), hours_time, fill="white",
                 font=proportional(CP437_FONT))
            text(draw, (16, current_y), ":", fill="white",
                 font=proportional(TINY_FONT))
            text(draw, (18, current_y), min_time, fill="white",
                 font=proportional(CP437_FONT))
        time.sleep(0.1)
        current_y += 1 if to_y > from_y else -1


def draw_time(device):
    hours = datetime.now().strftime('%H')
    minutes = datetime.now().strftime('%M')
    with canvas(device) as draw:
        text(draw, (0, 1), hours, fill="white",
             font=proportional(CP437_FONT))
        text(draw, (16, 1), ":", fill="white",
             font=proportional(TINY_FONT))
        text(draw, (18, 1), minutes, fill="white",
             font=proportional(CP437_FONT))


def minute_change(device):
    #  When we reach a minute change and animate it.
    hours = datetime.now().strftime('%H')
    minutes = datetime.now().strftime('%M')

    def helper(current_y):
        with canvas(device) as draw:
            text(draw, (0, 1), hours, fill="white",
                 font=proportional(CP437_FONT))
            text(draw, (15, 1), ":", fill="white",
                 font=proportional(TINY_FONT))
            text(draw, (17, current_y), minutes, fill="white",
                 font=proportional(CP437_FONT))
            time.sleep(0.1)

    # for current_y in range(1, 9):
    #        helper(current_y)
    minutes = datetime.now().strftime('%M')
    for current_y in range(9, 0, -1):
        helper(current_y)


def format_tides():
    tides = get_tides()
    m = '>Moon: {}%, {}'.format(tides['moon']['pct'], tides['moon']['phase'])
    td = ["{} {}".format(item.get('desc').replace('high', chr(24)).replace('low', chr(25)), item.get('ts'))
          for item in tides['tides']]
    t = '>Tides at {}: {}'.format(tides['location'], ", ".join(td))
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
                return ">Out T: {}{}C @ {}%".format(th.get('temperature_C'),
                                                    degree_sign,
                                                    th.get('humidity'))
    else:
        return ''


def showtime():
    #  setup display
    serial = spi(port=0, device=0)
    device = max7219(serial, cascaded=4, block_orientation=0, rotate=0)
    device.contrast(4)
    device.persist = True

    # between 6 and 10 show trains
    present = datetime.now()
    if (present.hour >= 6 and present.hour <= 10):
        #  show next three trains
        train_times = [tm.strftime('%H:%M') for tm in get_trains()[:3]]
        trains = ', '.join(train_times)
        show_message(device, '>Trains: ' + trains, fill="white",
                     font=proportional(CP437_FONT))
    weather = get_weather()
    show_message(device, '>Weather: ' + weather, fill="white",
                 font=proportional(CP437_FONT))
    show_message(device, read_sensor_data(), fill="white",
                 font=proportional(CP437_FONT))
    show_message(device, format_tides(), fill="white",
                 font=proportional(CP437_FONT))
    show_message(device, datetime.now().strftime("%a %d %b %Y"), fill="white",
                 font=proportional(CP437_FONT))
    minute_change(device)
