#!/usr/bin/env python3

# standard library
import os
import json
from datetime import datetime

#  my utility libraries
from .trains_util import get_trains
from .weather_util import get_weather
from .tides_util import get_tides


def format_tides():
    tides = get_tides()
    m = 'Moon: {}%, {}'.format(tides['moon']['pct'], tides['moon']['phase'])
    td = ["{} {}".format(item.get('desc'), item.get('ts'))
          for item in tides['tides']]
    t = 'Tides at {}: {}'.format(tides['location'], ", ".join(td))
    return "{}, {}".format(m, t)


def read_sensor_data():
    """
    Read Temperature and Humidity Sensor data and display.
    Prologue-TH wireless outdoor sensor is being used.
    rtl_433 utility will read the data via radio data channel
    and save the output to the file as a series of json objects.
    The command is scheduled in Cron:
    > rtl_433 -f 433920000 -R 03 -E quit -F json
    """
    filename = 'prologue/prologue.json'
    degree_sign = u"\N{DEGREE SIGN}"
    if os.path.exists(filename):
        with open(filename) as f:
            data = f.readlines()[-1]
            if data:
                th = json.loads(data)
                return "Out: {}{} @ {}%".format(th.get('temperature_C'),
                                                  degree_sign,
                                                  th.get('humidity'))


def showtime():
    # between 6 and 10 show trains
    present = datetime.now()
    print('Time: {}'.format(present.strftime('%H:%M')))
    if (present):
        #  show next three trains
        train_times = [tm.strftime('%H:%M') for tm in get_trains()[:3]]
        trains = ', '.join(train_times)
        print('Trains: {}'.format(trains))
        weather = get_weather()
        print('Weather: {}'.format(weather))
        print(format_tides())
        print(read_sensor_data())
