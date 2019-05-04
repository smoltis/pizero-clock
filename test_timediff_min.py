import unittest
from datetime import datetime
import pytz
from trains_util import timediff_min


class TestTimeDiffMethods(unittest.TestCase):

    def test_timediff_pos(self):
        fmt = '%Y-%m-%d %H:%M:%S'
        d1 = datetime.strptime('2010-01-01 17:31:22', fmt)
        d2 = datetime.strptime('2010-01-03 20:15:14', fmt)
        actual = timediff_min(d1, d2)
        self.assertAlmostEqual(actual, 3043, delta=0.99)

    def test_timediff_neg(self):
        fmt = '%Y-%m-%d %H:%M:%S'
        d1 = datetime.strptime('2010-01-01 17:31:22', fmt)
        d2 = datetime.strptime('2010-01-03 20:15:14', fmt)
        actual = timediff_min(d2, d1)
        self.assertAlmostEqual(actual, -3043, delta=0.99)

    def test_timediff_eq(self):
        fmt = '%Y-%m-%d %H:%M:%S'
        d1 = datetime.strptime("2010-01-01 17:31:22", fmt)
        d2 = datetime.strptime("2010-01-01 17:31:22", fmt)
        actual = timediff_min(d1, d2)
        self.assertEqual(actual, 0)

    def test_timediff_type(self):
        s1 = 'hello'
        s2 = 'world'
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            timediff_min(s1, s2)

    def test_timediff_tz_native(self):
        fmt = '%Y-%m-%d %H:%M:%S'
        d1 = datetime.strptime("2010-01-01 17:31:22", fmt)  # offset-naive
        utc = pytz.UTC
        d2 = datetime.strptime("2010-01-03 20:15:14", fmt)  
        d2 = utc.localize(d2)  # offset-aware
        actual = timediff_min(d1, d2)
        self.assertAlmostEqual(actual, 3043, delta=0.99)


if __name__ == '__main__':
    unittest.main()
