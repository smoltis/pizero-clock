import unittest
from weather_util import get_weather


class TestGetWeatherMethod(unittest.TestCase):

    def test_not_empty(self):
        actual = get_weather()
        self.assertTrue(len(actual) > 10)


if __name__ == '__main__':
    unittest.main()
