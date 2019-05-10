import shelve
from openweathermap import OWM
from datetime import datetime
from timeint_util import timediff_min


def get_weather():
    #  use cache here
    with shelve.open("weather.cache", writeback=True) as cached_weather:
        # find out if cache is stale
        present = datetime.now()
        # every 3h refresh
        dt_key = list(cached_weather.keys())
        if dt_key:
            key = datetime.strptime(dt_key[0], '%Y-%m-%d %H:%M:%S')
            if timediff_min(key, present) <= 3*60:
                weather = cached_weather[dt_key[0]]
        else:
            #  if stale refresh cache
            obj = OWM()
            weather, dt = obj.get_weather()
            cached_weather[str(dt)] = weather

    return weather