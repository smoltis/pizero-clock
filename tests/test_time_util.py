import pytest
from datetime import datetime
import pytz
from .context import showtime
from showtime.timeint_util import timediff_min, UtcTzConvert
from dateutil import tz

def test_timediff_pos():
    fmt = '%Y-%m-%d %H:%M:%S'
    d1 = datetime.strptime('2010-01-01 17:31:22', fmt)
    d2 = datetime.strptime('2010-01-03 20:15:14', fmt)
    actual = timediff_min(d1, d2)
    pytest.approx(actual, 0.01) == 3043


def test_timediff_neg():
    fmt = '%Y-%m-%d %H:%M:%S'
    d1 = datetime.strptime('2010-01-01 17:31:22', fmt)
    d2 = datetime.strptime('2010-01-03 20:15:14', fmt)
    actual = timediff_min(d2, d1)
    pytest.approx(actual, 0.01) == -3043


def test_timediff_eq():
    fmt = '%Y-%m-%d %H:%M:%S'
    d1 = datetime.strptime("2010-01-01 17:31:22", fmt)
    d2 = datetime.strptime("2010-01-01 17:31:22", fmt)
    actual = timediff_min(d1, d2)
    assert actual == 0


def test_timediff_type():
    s1 = 'hello'
    s2 = 'world'
    # check that s.split fails when the separator is not a string
    with pytest.raises(TypeError):
        timediff_min(s1, s2)


def test_timediff_tz_native():
    fmt = '%Y-%m-%d %H:%M:%S'
    d1 = datetime.strptime("2010-01-01 17:31:22", fmt)  # offset-naive
    utc = pytz.UTC
    d2 = datetime.strptime("2010-01-03 20:15:14", fmt)
    d2 = utc.localize(d2)  # offset-aware
    actual = timediff_min(d1, d2)
    pytest.approx(actual, 0.01) == 3043


def test_from_timestamp_conversion():
    expected = datetime.now(tz=tz.gettz('Australia/Sydney'))
    ts = expected.timestamp()
    actual = UtcTzConvert().from_timestamp(ts)
    assert expected == actual
