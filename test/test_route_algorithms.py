import unittest

#import source_file.route_algorithms as best_price
from source_file.aircrafts_dictionary import AircraftDictionaryParent
from source_file.country_currencies import CountryCurrenciesDictionaryParent
from source_file.currency_rates import CurrencyRatesDictionaryParent
from source_file.routes_algorithms import Routes
from source_file.airport_atlas import AirportAtlas


class TestRouteAlgorithms(unittest.TestCase):

    def setUp(self):
        self.airports = ['DUB', 'ZAZ', 'JFK', 'CDG']
        self.route = {1: ('ALL', 'DUB', 4567, 3454),
                      2: ('DUB', 'AAL', 4567, 3454),
                      3: ('DER', 'DB', 4567, 3454)}
        self.list_aircrafts = ['A319', '777', 'A320', 'A321', 'F50']
        self.atlas = AirportAtlas('../csv_files/airport.csv')
        self.curr_rates = CurrencyRatesDictionaryParent('../csv_files/currencyrates.csv')
        self.country_curr = CountryCurrenciesDictionaryParent('../csv_files/countrycurrency.csv')
        self.aircrafts = AircraftDictionaryParent('../csv_files/aircraft.csv')
        self.routes_algo = Routes(self.aircrafts, self.atlas, self.curr_rates, self.country_curr)

    def test_if_element_in_dictionary_is_deleted_from_input_list(self):
        """Tests if the self.input list will be modified as DUB code is already in the dictionary and therefore cancel from list"""
        self.assertListEqual(self.routes_algo.modify_list(self.airports, self.route), ['ZAZ', 'JFK', 'CDG'])

    def test_count_how_many_times_airport_code_is_in_given_dictionary(self):
        self.assertEqual(self.routes_algo.count_visited_airports(self.route, self.airports[0]), 1)

    def test_algorithm_shortest_distance(self):
        self.route = self.routes_algo.find_shortest_route('777', 'LHR', self.airports)
        self.expected_route = {1: ('LHR', 'CDG'), 2 : ('CDG', 'DUB'), 3:('DUB', 'ZAZ'), 4: ('ZAZ', 'JFK'), 5 : ('JFK', 'LHR')}
        self.route_only_airport_codes = {}
        for i, j in self.route.items():
            self.route_only_airport_codes[i] = (j[0], j[1])

        self.assertDictEqual(self.route_only_airport_codes, self.expected_route)

    def test_algorithm_route_with_possible_stopover(self):
        """Tests the algorithm find_route_with_possible_stopover. For a series of aircrafts it checks that the route found it will be
        the same as expected (in this case). Then it checks if for a aircraft with short range the output it will be an empty
        dictionary as no routes are found"""
        for aircr in self.list_aircrafts:
            self.route = self.routes_algo.find_route_with_possible_stopover(aircr, 'LHR', self.airports)
            self.expected_route = {1: ('LHR', 'DUB'), 2: ('DUB', 'JFK'), 3: ('JFK', 'ZAZ'), 4: ('ZAZ', 'CDG'), 5: ('CDG', 'LHR')}
            self.route_only_airport_codes = {}
            for i, j in self.route.items():
                self.route_only_airport_codes[i] = (j[0], j[1])
            if aircr != 'F50':
                self.assertDictEqual(self.route_only_airport_codes, self.expected_route)
            else:
                self.assertDictEqual(self.route_only_airport_codes, {})

    def test_calculate_longest_distance(self):
        self.expected_total = 28766
        self.assertEqual(self.routes_algo.calculate_total_longest_distance([*self.airports, 'AAL']), self.expected_total)

    def test_if_for_a_list_finds_cheapest_airport_at_min_distance(self):
        self.home = 'DUB'
        self.airp_list1 = ['LHR', 'JFK', 'CDG', 'AAL']
        self.airp_list2 = ['ZAZ', 'EBO', 'CDG', 'JIK']
        self.assertEqual(
            self.routes_algo.get_cheapest_airport_at_min_distance(self.home, self.airp_list1),
            'AAL')
        self.assertEqual(
            self.routes_algo.get_cheapest_airport_at_min_distance(self.home, self.airp_list2),
            'CDG')

    def test_algorithm_route_cheapest_fuel(self):
        """Tests the algorithm find route considering cheapest fuel, where it expected that in AAL the tank will be filled it up
        and this will be enough for the rest of route"""
        self.route = self.routes_algo.find_route_saving_fuel('777', 'DUB', ['AAL', 'CDG', 'ZAZ', 'LHR'])
        fuel = self.routes_algo.calculate_sum_km_or_fuel_in_best_route(self.route, 4)
        self.assertEqual(int(fuel), 91493)

    def test_stopover_route(self):
        self.airports = ['GME', 'CRL', 'OMO', 'FBD']
        self.expected_route = {1: ('LWN', 'GME'), 2: ('GME', 'CRL'),
                               3: ('CRL', 'GME'), 4: ('GME', 'FBD'),
                               5: ('FBD', 'OMO'), 6: ('OMO', 'LWN')}
        self.route = self.routes_algo.find_route_with_possible_stopover('737-600', 'LWN', self.airports)
        self.route_only_airport_codes = {}
        for i, j in self.route.items():
            self.route_only_airport_codes[i] = (j[0], j[1])

        self.assertDictEqual(self.route_only_airport_codes, self.expected_route)
    def tearDown(self):
        print("Test on route algorithms completed")