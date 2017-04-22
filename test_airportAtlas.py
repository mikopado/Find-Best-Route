import unittest
from airport_atlas import AirportAtlas
from airport import Airport
from custom_exceptions import *


class TestAirportAtlas(unittest.TestCase):

    def setUp(self):
        self.atl = AirportAtlas("airport.csv")
        self.list_known_air = (("DUB", "SYD", 17215), ("LHR", "JFK", 5539),
                               ("CDG", "AAL", 1021))

        self.list_all_codes = []
        for i in self.atl.data_dict.keys():
            self.list_all_codes.append(i)

    def test_distance_beetween_different_airports(self):
        for i, j, dist in self.list_known_air:
            self.assertEqual(self.atl.get_distance_between_airports(i, j), dist)

    def test_distance_same_airport(self):
        for i in self.list_all_codes:
            self.assertEqual(self.atl.get_distance_between_airports(i, i), 0)

    def test_invalid_airport_code(self):
        with self.assertRaises(InvalidCodeError):
            self.atl.get_object_from_key("D")

    def test_valid_airport_codes(self):
        for i in self.atl.data_dict.keys():
            self.assertTrue(self.atl.get_object_from_key(i))

    def test_get_airport_from_code(self):
        code = 'DUB'
        self.airp = Airport('DUB', 'Dublin', 'Ireland','Dublin', 53.421333, -6.270075)
        self.assertEqual(self.atl.get_object_from_key(code).get_country(), self.airp.get_country())

    def test_if_exception_raises_for_csv_not_found(self):
        with self.assertRaises(FileNotExistError):
            self.atl = AirportAtlas("airpor.cs")
        # except FileNotFoundError:
        #     self.fail('csv not found test failed')

    def test_if_exception_raises_for_invalid_format_csvfile(self):
        with self.assertRaises(FileFormatError):
            self.atl = AirportAtlas("aircraft.csv")

    def test_get_max_distance_airports(self):
        self.airp_list = ['LHR', 'JFK','CDG','AAL']
        self.airp_list2 = ['DUB','DUB','DUB','DUB']
        self.assertEqual(self.atl.get_airport_at_max_distance('DUB', self.airp_list), 'JFK')
        self.assertEqual(self.atl.get_airport_at_max_distance('DUB', self.airp_list2), 'DUB')
        self.assertNotEqual(self.atl.get_airport_at_max_distance('DUB', self.airp_list), 'AAL')

if __name__ == "__main__":
    unittest.main()
