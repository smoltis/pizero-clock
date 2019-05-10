#  my utility libraries
from nswtrains import NswTrains
import shelve
from timeint_util import timediff_min
from datetime import datetime


def get_trains():
    #  use cache here
    with shelve.open("nswtrains.cache", writeback=True) as cached_trains:
        # find out if cache is stale
        present = datetime.now()
        #  trains after +10 min from now
        next_trains = []
        if (cached_trains.keys()):
            next_trains = [train for train in cached_trains.values() if timediff_min(present, train) >= 10]

        #  if stale refresh cache
        if len(next_trains) < 3:
            obj = NswTrains()
            next_trains = obj.get_trains()
            for key, item in enumerate(next_trains):
                cached_trains[str(key)] = item

    return sorted(next_trains)
    