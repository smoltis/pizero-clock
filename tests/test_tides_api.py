from .context import showtime
from showtime.tidesapi import TidesApiClient
from datetime import datetime
from showtime.tides_util import get_tides

def test_tides_client_returns_result():
    dt = datetime.utcnow()
    start_date = '{0}-{1}-{2}'.format(dt.year, dt.month, dt.day)
    actual = TidesApiClient(start_date).get_tides()
    assert len(actual.get('location', None)) > 3
    assert len(actual.get('tides')) > 1
    assert actual.get('moon').get('pct', None) >= 0


def test_response_array_filter():
    timeZoneOffset = 36000
    ts = 1595982031.162842 + timeZoneOffset
    a = [{'dateTime': 1595980800}, {'dateTime': 1596067200}, {'dateTime': 1596153600}]
    actual = [x for x in a if x['dateTime'] < ts]
    assert len(actual) == 1


def test_tides_util_get_tides_returns_result():
    actual = get_tides()
    assert (len(actual.get('location', None)) > 3) is True