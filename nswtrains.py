
import requests
from datetime import datetime
from dateutil import tz
import nswtrains_secrets


class NswTrains(object):

    def __init__(self,
                    url=nswtrains_secrets.NSW_TRAINS_URL,
                    local_tz=nswtrains_secrets.LOCAL_TZ):
        self.url = url
        self.local_tz = local_tz
        self._set_tz()

    def _get_response(self):
        r = requests.get(self.url)
        return r.json()

    def _set_tz(self):
        # Hardcode UTC zone
        self.from_zone = tz.gettz('UTC')
        self.to_zone = tz.gettz(self.local_tz)

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
            local_time = self._convert_tz(departure_utc)
            result.append(local_time)
        return result

    def _convert_tz(self, dt_utc):
        utc = datetime.strptime(dt_utc, '%Y-%m-%dT%H:%M:%SZ')
        utc = utc.replace(tzinfo=self.from_zone)
        local_time = utc.astimezone(self.to_zone)
        return local_time.replace(tzinfo=None)

    def _format_result(self, items):
        #  [item.strftime('%H:%M') for item in items]
        return items
