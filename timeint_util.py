from dateutil import tz
from datetime import datetime


def timediff_min(start_dt, end_dt):
    #  convert to datetime native
    diff = (end_dt.replace(tzinfo=None) - start_dt.replace(tzinfo=None))
    diff_min = (diff.days * 24 * 60) + (diff.seconds/60)
    return diff_min


class UtcTzConvert(object):
    def __init__(self, local_tz='Australia/Sydney'):
        self._set_tz(local_tz)

    def _set_tz(self, local_tz):
        # Hardcode UTC zone
        self.from_zone = tz.gettz('UTC')
        self.to_zone = tz.gettz(local_tz)

    def convert(self, dt_utc):
        utc = dt_utc.replace(tzinfo=self.from_zone)
        local_time = utc.astimezone(self.to_zone)
        return local_time.replace(tzinfo=None)  # return datetime native
