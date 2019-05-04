import unittest
from trains_util import get_trains


class TestGetTrainsMethod(unittest.TestCase):

    def test_not_empty(self):
        actual = get_trains()
        self.assertEqual(len(actual), 3)


if __name__ == '__main__':
    unittest.main()
