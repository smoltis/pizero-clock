#!/usr/bin/env python

import time
import json
from datetime import datetime

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT

from nswtrains import NswTrains

'''
# optionally read temperature and humidity sensor data
def read_sensor():
    with open("/home/pi/sensors/prologue.json","r") as f:
        lines = f.read().splitlines()
        json_string = lines[-1]
    parsed_json = json.loads(json_string)
    temperature_in = parsed_json['temperature_C']
    humidity_in = parsed_json['humidity']
    return temperature_in, humidity_in    
'''

def animation_dt(device, from_y, to_y, dt):
    #  Animate the whole thing, moving it into/out of the abyss.
    hourstime = dt.strftime('%H')
    mintime = dt.strftime('%M')
    current_y = from_y
    while current_y != to_y:
        with canvas(device) as draw:
            text(draw, (0, 0), "l", fill="white", font=proportional(TINY_FONT))
            text(draw, (1, current_y), hourstime, fill="white", font=proportional(CP437_FONT))
            text(draw, (16, current_y), ":", fill="white", font=proportional(TINY_FONT))
            text(draw, (18, current_y), mintime, fill="white", font=proportional(CP437_FONT))
        time.sleep(0.1)
        current_y += 1 if to_y > from_y else -1

def show_trains(device):
        #  use cache here
        #cached_trains = read_trains_cache()
        #if not cached_trains:
        #        write_train_cache()

        # find out if cache is stale
        #present = datetime.now()
        #next_trains = [train for train in cached_trains if train > present]
        
        #  if stale refresh cache for next itereation
        #if len(next_trains) < 3:
        #        write_train_cache()
        obj = NswTrains()
        next_trains = obj.get_trains()[:3]
        #  show next three trains
        for train_time in next_trains:
                animation_dt(device, 9, 0, train_time)
                time.sleep(3)

def my_dt_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def read_trains_cache():
        result = []
        try:
                with open("train_cache.json","r") as f:
                        json_string = f.read()
                        parsed_json = json.loads(json_string)
                        result = [datetime.strptime(item, "%Y-%m-%d %H:%M:%S.%f") for item in parsed_json['trains']]
        except IOError:
                pass
        return result


def write_train_cache():
        obj = NswTrains()
        trains = obj.get_trains()
        with open("train_cache.json","w") as f:
                d = {}
                d['trains'] = []
                f.write(json.dumps(trains, default = my_dt_converter))

def draw_time(device):
        hours = datetime.now().strftime('%H')
        minutes = datetime.now().strftime('%M')
        with canvas(device) as draw:
                text(draw, (0, 1), hours, fill="white", font=proportional(CP437_FONT))
                text(draw, (16, 1), ":", fill="white", font=proportional(TINY_FONT))
                text(draw, (18, 1), minutes, fill="white", font=proportional(CP437_FONT))

def minute_change(device):
        #  When we reach a minute change and animate it.
        hours = datetime.now().strftime('%H')
        minutes = datetime.now().strftime('%M')

        def helper(current_y):
                with canvas(device) as draw:
                        text(draw, (0, 1), hours, fill="white", font=proportional(CP437_FONT))
                        text(draw, (15, 1), ":", fill="white", font=proportional(TINY_FONT))
                        text(draw, (17, current_y), minutes, fill="white", font=proportional(CP437_FONT))
                        time.sleep(0.1)

        #for current_y in range(1, 9):
        #        helper(current_y)
        minutes = datetime.now().strftime('%M')
        for current_y in range(9, 0, -1):
                helper(current_y)


if __name__ == '__main__':
        serial = spi(port=0, device=0)
        device = max7219(serial, cascaded=4, block_orientation=0, rotate=0)
        device.contrast(4)
        device.persist = True

        minute_change(device)
        # between 6 and 10 show trains
        present = datetime.now()
        if (present.hour >= 6 and present.hour<=10):
                time.sleep(10)
                show_message(device, 'Trains:', fill="white", font=proportional(CP437_FONT))
                show_trains(device)
                minute_change(device)


