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
        self.airp_list = ['LHR', 'JFK', 'CDG', 'AAL']
        self.airp_list2 = ['DUB', 'DUB', 'DUB', 'DUB']

    def test_distance_beetween_different_airports(self):
        """Tests distnace between airports methods considering a list of airports"""
        for i, j, dist in self.list_known_air:
            self.assertEqual(self.atl.get_distance_between_airports(i, j), dist)

    def test_distance_same_airport(self):
        """Tests get_distance_between_airports methods with same airport"""
        for i in self.list_all_codes:
            self.assertEqual(self.atl.get_distance_between_airports(i, i), 0)

    def test_invalid_airport_code(self):
        """Tests if the InvalidCodeError is raising when input an invalid airport code"""
        with self.assertRaises(InvalidCodeError):
            self.atl.get_object_from_key("D")

    def test_valid_airport_codes(self):
        for i in self.atl.data_dict.keys():
            self.assertTrue(self.atl.get_object_from_key(i))

    def test_if_from_airport_code_get_a_valid_country(self):
        """Tests if from a given airport code it gets the correct country associated to it"""
        code = 'DUB'
        self.airp = Airport('DUB', 'Dublin', 'Ireland','Dublin', 53.421333, -6.270075)
        self.assertEqual(self.atl.get_object_from_key(code).get_country(), self.airp.get_country())

    def test_if_exception_raises_for_csv_not_found(self):
        """Tests if FileNotExistError raise when input a not existing csv file"""
        with self.assertRaises(FileNotExistError):
            self.atl = AirportAtlas("airpor.cs")

    def test_if_exception_raises_for_invalid_format_csvfile(self):
        with self.assertRaises(FileFormatError):
            self.atl = AirportAtlas("aircraft.csv")

    def test_if_get_airport_at_max_distance_from_alist_of_airports(self):
        self.assertEqual(self.atl.get_airport_at_max_distance('DUB', self.airp_list), 'JFK')
        self.assertEqual(self.atl.get_airport_at_max_distance('DUB', self.airp_list2), 'DUB')
        self.assertNotEqual(self.atl.get_airport_at_max_distance('DUB', self.airp_list), 'AAL')
    def tearDown(self):
        print("Test on airport atlas completed")


if __name__ == "__main__":
    unittest.main()
