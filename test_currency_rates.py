import unittest
from currency_rates import CurrencyRatesDictionary
from country_currencies import  CountryCurrenciesDictionary
from airport_atlas import AirportAtlas

class TestCurrency(unittest.TestCase):

    def setUp(self):
        self.rates = CurrencyRatesDictionary('currencyrates.csv')

        self.airports = AirportAtlas('airport.csv')
        self.currencies = CountryCurrenciesDictionary('countrycurrency.csv')
        self.list_airports = ['DUB', 'LHR', 'MMY', 'YQT', 'MOW']

    def test_get_rate_from_country(self):
        self.rate_list = []
        for code in self.list_airports:
            self.rate = self.rates.get_rate_from_country(code, self.airports, self.currencies)
            self.rate_list.append(self.rate)
        self.assertListEqual(self.rate_list, [1.0, 1.4029, 0.007822, 0.7423, 0.01524])

    def test_highest_rate(self):
        self.max_rate = 1.4029
        self.assertEqual(self.rates.get_highest_rate_from_airport_codes(self.list_airports,
                                                                        self.airports, self.currencies), self.max_rate)
        for rate in [1.0, 0.007822, 0.7423, 0.01524]:
            self.assertNotEqual(self.rates.get_highest_rate_from_airport_codes(self.list_airports,
                                                                            self.airports, self.currencies), rate)
    def test_cheapest_rate(self):
        self.min_rate = 0.007822
        self.assertEqual(self.rates.get_cheapest_rate_from_airport_codes(self.list_airports,
                                                                        self.airports, self.currencies), self.min_rate)
        for rate in [1.0, 1.4029, 0.7423, 0.01524]:
            self.assertNotEqual(self.rates.get_cheapest_rate_from_airport_codes(self.list_airports,
                                                                        self.airports, self.currencies), rate)
