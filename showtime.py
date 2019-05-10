#!/usr/bin/env python3

# standard library
from datetime import datetime

#  my utility libraries
from trains_util import get_trains
from weather_util import get_weather


def minute_change():
    tm = datetime.now().strftime('%H:%M')
    print(tm)


if __name__ == '__main__':
    # between 6 and 10 show trains
    present = datetime.now()
    if (True):
        #  show next three trains
        train_times = [tm.strftime('%H:%M') for tm in get_trains()[:3]]
        trains = ', '.join(train_times)
        print('Trains: ' + trains)
        weather = get_weather()
        print('Weather: ' + weather)
    minute_change()
