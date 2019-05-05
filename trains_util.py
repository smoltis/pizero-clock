#  my utility libraries
from nswtrains import NswTrains
import shelve
from datetime import datetime


def timediff_min(start_dt, end_dt):
    diff = (end_dt.replace(tzinfo=None) - start_dt.replace(tzinfo=None))
    diff_min = (diff.days * 24 * 60) + (diff.seconds/60)
    return diff_min


def get_trains():
    #  use cache here
    cached_trains = shelve.open("nswtrains.cache", writeback=True)
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
    # save to cache
    cached_trains.close()
    return next_trains
    