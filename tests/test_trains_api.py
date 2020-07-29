from .context import showtime
from showtime.trains_util import get_trains


def test_get_trains_returns_result():
    actual = get_trains()
    assert len(actual) > 1
