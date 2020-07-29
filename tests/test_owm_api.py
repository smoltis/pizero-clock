from .context import showtime
from showtime.weather_util import get_weather


def test_get_weather_returns_result():
    actual = get_weather()
    assert (len(actual) > 10) is True
