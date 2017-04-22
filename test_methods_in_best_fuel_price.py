import unittest
import best_routes as best_price
from aircrafts_dictionary import AircraftDictionary
from airport_atlas import AirportAtlas
from currency_rates import CurrencyRatesDictionary
from country_currencies import CountryCurrenciesDictionary

class TestBestRoutes(unittest.TestCase):

    def setUp(self):
        self.input_list = ['DUB', 'ZAZ', 'JFK', 'CDG']
        self.input_dict = {1: ('ALL', 'DUB', 4567, 3454),
                           2: ('DUB', 'AAL', 4567, 3454),
                           3: ('DER', 'DB', 4567, 3454)}

    def test_modify_list(self):
        self.assertListEqual(best_price.modify_list(self.input_list, self.input_dict), ['ZAZ', 'JFK','CDG'])

    def test_count_airport_in_dict(self):
        self.assertEqual(best_price.count_visited_airports(self.input_dict, self.input_list[0]), 1)

    def test_best_route_min_distance(self):
        self.route = best_price.find_shortest_route('777', 'LHR', self.input_list, AirportAtlas('airport.csv'),
                                                    AircraftDictionary('aircraft.csv'),
                                                    CurrencyRatesDictionary('currencyrates.csv'),
                                                    CountryCurrenciesDictionary('countrycurrency.csv'))
        self.expected_route = {1: ('LHR', 'CDG'), 2 : ('CDG', 'DUB'), 3:('DUB', 'ZAZ'), 4: ('ZAZ', 'JFK'), 5 : ('JFK', 'LHR')}
        self.route_only_airport_codes = {}
        for i, j in self.route.items():
            self.route_only_airport_codes[i] = (j[0], j[1])

        self.assertDictEqual(self.route_only_airport_codes, self.expected_route)

    def test_best_route_possible_stopover(self):
        list_aircrafts = ['A319', '777', 'A320', 'A321', 'F50']
        for aircr in list_aircrafts:
            self.route = best_price.find_route_with_possible_stopover(aircr, 'LHR', self.input_list,
                                                                  AirportAtlas('airport.csv'),
                                                                  AircraftDictionary('aircraft.csv'),
                                                                  CurrencyRatesDictionary('currencyrates.csv'),
                                                                  CountryCurrenciesDictionary('countrycurrency.csv'))
            self.expected_route = {1: ('LHR', 'DUB'), 2: ('DUB', 'JFK'), 3: ('JFK', 'ZAZ'), 4: ('ZAZ', 'CDG'), 5: ('CDG', 'LHR')}
            self.route_only_airport_codes = {}
            for i, j in self.route.items():
                self.route_only_airport_codes[i] = (j[0], j[1])
            if aircr != 'F50':
                self.assertDictEqual(self.route_only_airport_codes, self.expected_route)
            else:
                self.assertDictEqual(self.route_only_airport_codes, {})