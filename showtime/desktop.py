#!/usr/bin/env python3

# standard library
from datetime import datetime

#  my utility libraries
from .trains_util import get_trains
from .weather_util import get_weather
from .tides_util import get_tides

def format_tides():
    tides = get_tides()
    m = 'Moon: {}%, {}'.format(tides['moon']['pct'], tides['moon']['phase'])
    td = ["{} {}".format(item.get('desc'), item.get('ts')) for item in tides['tides']]
    t = 'Tides at {}: {}'.format(tides['location'], ", ".join(td))
    return "{} {}".format(m, t)


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
