# https://tides.willyweather.com.au/graphs/data.json?startDate=2020-7-28&graph=outlook:5,location:19170,series=order:0,id:sunrisesunset,type:forecast,series=order:1,id:tides,type:forecast
import requests
from datetime import datetime
from .tides_secrets import TIDES_API_URL
from .timeint_util import UtcTzConvert


class TidesApiClient(object):

    def __init__(self,
                 start_date="2020-7-28",
                 location=19170,
                 url=TIDES_API_URL):
        self.location = location
        self.start_date = start_date
        self.url = url.format(start_date, location)

    def _get_response(self):
        r = requests.get(self.url)
        return r.json()

    def get_tides(self):
        response = self._get_response()
        result = self._parse_response(response)
        return self._format_result(result)

    def _parse_response(self, response):
        location_name = response['data']['location']['name']
        timeZoneOffset = response['data']['location']['timeZoneOffset']
        tides_raw = response['data']['forecastGraphs']['tides']['dataConfig']['series']['groups']
        # find today's info
        ts = datetime.timestamp(datetime.utcnow()) + int(timeZoneOffset)
        tides_today = [data for data in tides_raw if int(data['dateTime']) < int(ts)]
        moon = tides_info = None

        if not tides_today:
            return None, None

        tides_info = [point for point in tides_today[0]['points']
                      if point['description'] != '']
        moon = {
                "pct": tides_today[0]['overlays'][0]['data']['percentageFull'],
                "phase": tides_today[0]['overlays'][0]['data']['phase']
            }
        units = response['data']['forecastGraphs']['tides']['units']['height']
        tides = [
                {
                    "ts": UtcTzConvert()\
                            .from_timestamp(mark.get('x'))\
                            .strftime('%H:%M'),
                    "desc": mark.get('description'),
                    "height": mark.get('y'),
                    "units": units
                    }
                for mark in tides_info]
        return {"location": location_name, "tides": tides, "moon": moon}

    def _format_result(self, items):
        #  [item.strftime('%H:%M') for item in items]
        return items
