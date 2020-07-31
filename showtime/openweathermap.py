import requests
from datetime import datetime
from .owm_secrets import API_URL
from .timeint_util import UtcTzConvert

''' API Response Parameters:
coord
coord.lon City geo location, longitude
coord.lat City geo location, latitude

weather (more info Weather condition codes)
weather.id Weather condition id
weather.main Group of weather parameters (Rain, Snow, Extreme etc.)
weather.description Weather condition within the group
weather.icon Weather icon id

base Internal parameter

main
main.temp Temperature. Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit.
main.pressure Atmospheric pressure (on the sea level, if there is no sea_level or grnd_level data), hPa
main.humidity Humidity, %
main.temp_min Minimum temperature at the moment. This is deviation from current temp that is possible for large cities and megalopolises geographically expanded (use these parameter optionally). Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit.
main.temp_max Maximum temperature at the moment. This is deviation from current temp that is possible for large cities and megalopolises geographically expanded (use these parameter optionally). Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit.
main.sea_level Atmospheric pressure on the sea level, hPa
main.grnd_level Atmospheric pressure on the ground level, hPa

wind
wind.speed Wind speed. Unit Default: meter/sec, Metric: meter/sec, Imperial: miles/hour.
wind.deg Wind direction, degrees (meteorological)

clouds
clouds.all Cloudiness, %

rain
rain.1h Rain volume for the last 1 hour, mm
rain.3h Rain volume for the last 3 hours, mm

snow
snow.1h Snow volume for the last 1 hour, mm
snow.3h Snow volume for the last 3 hours, mm

dt Time of data calculation, unix, UTC

sys
sys.type Internal parameter
sys.id Internal parameter
sys.message Internal parameter
sys.country Country code (GB, JP etc.)
sys.sunrise Sunrise time, unix, UTC
sys.sunset Sunset time, unix, UTC

id City ID
name City name
cod Internal parameter
'''


class OWM(object):

    def __init__(self, url=API_URL):
        self.url = url

    def get_weather(self):
        response = self._get_response()
        result, ts = self._parse_response(response)
        return result, ts

    def _get_response(self):
        r = requests.get(self.url)
        return r.json()

    def _parse_response(self, response):
        tzc = UtcTzConvert()
        sr = tzc.convert(datetime.utcfromtimestamp(response['sys']['sunrise']))
        ss = tzc.convert(datetime.utcfromtimestamp(response['sys']['sunset']))
        ts = tzc.convert(datetime.utcfromtimestamp(response['dt']))

        weather = \
            "{}, {}°C @ {}%, cloudiness {}%, sunrise {}, sunset {}".format(
                response['weather'][0]['description'],
                response['main']['temp'],
                response['main']['humidity'],
                response['clouds']['all'],
                sr.strftime('%H:%M'),
                ss.strftime('%H:%M'))
        return weather, ts
