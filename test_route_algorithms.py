import unittest
import route_algorithms as best_price
from aircrafts_dictionary import AircraftDictionaryParent
from airport_atlas import AirportAtlas
from currency_rates import CurrencyRatesDictionaryParent
from country_currencies import CountryCurrenciesDictionaryParent


class TestRouteAlgorithms(unittest.TestCase):

    def setUp(self):
        self.input_list = ['DUB', 'ZAZ', 'JFK', 'CDG']
        self.input_dict = {1: ('ALL', 'DUB', 4567, 3454),
                           2: ('DUB', 'AAL', 4567, 3454),
                           3: ('DER', 'DB', 4567, 3454)}
        self.list_aircrafts = ['A319', '777', 'A320', 'A321', 'F50']
        self.atlas = AirportAtlas('airport.csv')
        self.curr_rates = CurrencyRatesDictionaryParent('currencyrates.csv')
        self.country_curr = CountryCurrenciesDictionaryParent('countrycurrency.csv')
        self.aircrafts = AircraftDictionaryParent('aircraft.csv')

    def test_if_element_in_dictionary_is_deleted_from_input_list(self):
        """Tests if the self.input list will be modified as DUB code is already in the dictionary and therefore cancel from list"""
        self.assertListEqual(best_price.modify_list(self.input_list, self.input_dict), ['ZAZ', 'JFK','CDG'])

    def test_count_how_many_times_airport_code_is_in_given_dictionary(self):
        self.assertEqual(best_price.count_visited_airports(self.input_dict, self.input_list[0]), 1)

    def test_algorithm_shortest_distance(self):
        self.route = best_price.find_shortest_route('777', 'LHR', self.input_list, self.atlas,
                                                    self.aircrafts,
                                                    self.curr_rates,
                                                    self.country_curr)
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
            self.route = best_price.find_route_with_possible_stopover(aircr, 'LHR', self.input_list,
                                                                  self.atlas,
                                                                  self.aircrafts,
                                                                  self.curr_rates,
                                                                  self.country_curr)
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
        self.assertEqual(best_price.calculate_total_longest_distance([*self.input_list, 'AAL']), self.expected_total)

    def test_if_for_a_list_finds_cheapest_airport_at_min_distance(self):
        self.home = 'DUB'
        self.airp_list1 = ['LHR', 'JFK', 'CDG', 'AAL']
        self.airp_list2 = ['ZAZ', 'EBO', 'CDG', 'JIK']
        self.assertEqual(
            best_price.get_cheapest_airport_at_min_distance(self.home, self.airp_list1, self.atlas, self.curr_rates, self.country_curr),
            'AAL')
        self.assertEqual(
            best_price.get_cheapest_airport_at_min_distance(self.home, self.airp_list2, self.atlas, self.curr_rates, self.country_curr),
            'CDG')

    def test_algorithm_route_cheapest_fuel(self):
        """Tests the algorithm find route considering cheapest fuel, where it expected that in AAL the tank will be filled it up
        and this will be enough for the rest of route"""
        self.route = best_price.find_route_saving_fuel('777', 'DUB', ['AAL', 'CDG', 'ZAZ', 'LHR'],
                                                       self.atlas, self.aircrafts, self.curr_rates, self.country_curr)
        fuel = best_price.get_sum_of_dict_values(self.route, 4)
        self.assertEqual(int(fuel), 91493)

    def tearDown(self):
        print("Test on route algorithms completed")