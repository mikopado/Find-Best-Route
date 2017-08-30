import unittest

from source_file.airport import Airport


class TestAirport(unittest.TestCase):

    def test_invalid_latitude(self):
        self.airport = Airport("1", "Kennedy", "US", "New York", "a53.1234", "33.4567")
        self.assertEqual(self.airport.get_latitude(), 0.0)

    def test_invalid_longitude(self):
        self.airport = Airport(1, "Kennedy", "US", "New York", 53.1234, "a33.4567")
        self.assertEqual(self.airport.get_longitude(), 0.0)