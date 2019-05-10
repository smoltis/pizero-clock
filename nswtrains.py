
import requests
from datetime import datetime
from dateutil import tz
import nswtrains_secrets
from timeint_util import UtcTzConvert


class NswTrains(object):

    def __init__(self, url=nswtrains_secrets.NSW_TRAINS_URL):
        self.url = url

    def _get_response(self):
        r = requests.get(self.url)
        return r.json()

    def get_trains(self):
        response = self._get_response()
        result = self._parse_response(response)
        return self._format_result(result)

    def _parse_response(self, response):
        result = []
        for journey in response['journeys']:
            #  format: 2019-04-22T10:55:30Z
            departure_utc = journey['legs'][0]['origin']['departureTimePlanned']
            # fare = journey['fare']['tickets'][0]['properties']['priceTotalFare']
            # convert string to datetime object
            departure_utc = datetime.strptime(departure_utc, '%Y-%m-%dT%H:%M:%SZ')
            local_time = UtcTzConvert().convert(departure_utc)
            result.append(local_time)
        return result

    def _format_result(self, items):
        #  [item.strftime('%H:%M') for item in items]
        return items
