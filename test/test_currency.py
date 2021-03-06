import unittest

from source_file.country_currencies import CountryCurrenciesDictionaryParent


class TestCurrency(unittest.TestCase):
    def setUp(self):
        self.currencies = CountryCurrenciesDictionaryParent('../csv_files/countrycurrency.csv')
        self.list_of_countries = ['Italy', 'Spain', 'Germany', 'France', 'United States', 'Papua New Guinea', 'Russia']

    def test_get_country(self):
        for country in self.list_of_countries:
            self.currency = (self.currencies.get_object_from_key(country))
            self.assertEqual(self.currency.get_country(), country)
            self.assertNotEqual(self.currency.get_country(), 'United')
    def tearDown(self):
        print("Test on country currencies completed")