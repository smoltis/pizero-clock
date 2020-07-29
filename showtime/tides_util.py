from .tidesapi import TidesApiClient
import shelve
from .timeint_util import timediff_min
from datetime import datetime

CACHE_EXPIRY_MIN = 120


def get_tides():
    tides_info = None
    #  use cache here
    with shelve.open("tides.cache", writeback=True) as cached_items:
        # find if cache is stale
        present = datetime.now()
        refresh = False
        dt_key = list(cached_items.keys())
        if dt_key:
            key = datetime.strptime(dt_key[0], '%Y-%m-%d %H:%M:%S')
            if timediff_min(key, present) <= CACHE_EXPIRY_MIN:
                tides_info = cached_items[dt_key[0]]
            else:
                refresh = True
        else:
            refresh = True

        if refresh:
            #  if stale refresh cache
            dt = datetime.utcnow()
            start_date = '{0}-{1}-{2}'.format(dt.year, dt.month, dt.day)
            tides_info = TidesApiClient(start_date).get_tides()
            cached_items[present.strftime('%Y-%m-%d %H:%M:%S')] = tides_info

        return tides_info
