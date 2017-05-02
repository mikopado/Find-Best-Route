from parent_class_dictionary import ParentClassDictionary
from custom_exceptions import *


class CurrencyRatesDictionaryParent(ParentClassDictionary):

    def __init__(self, csv_file):
        self.data_dict = {}
        ParentClassDictionary.__init__(self, csv_file)

    def load_data(self, csv_file):
        try:
            file, records = self.open_csv_file(csv_file)
            try:
                for row in records:
                    rates = float(row['convert_to_euro']), float(row['convert_from_euro'])
                    self.data_dict[row['currency_alphabetic_code']] = rates
            except KeyError:
                raise FileFormatError("Columns are not matching! Wrong file format")
            finally:
                file.close()
        except FileNotFoundError:
            raise FileNotExistError('File not exists')

    def get_object_from_key(self, code):
        """Needs to override this method because for currency rates file the only data needed is 'convert to euro' column"""
        code.upper()
        if code in self.data_dict.keys():
            return self.data_dict[code][0]
        else:
            raise InvalidCodeError((code, " is not a valid code!"))

    def get_rate_from_country(self, airp_code, airp_dict, currency_dict):
        """Giving an airport code, retrieves the currency rate associated to the country where the airport is. In case
        it will not find any currency rates for the given country, the currency rate is set equal to 1.0 (assumption)"""
        try:
            code = currency_dict.get_object_from_key(airp_dict.get_object_from_key(airp_code).get_country()).get_code()
        except AttributeError:
            return 1.0
        else:
            return self.get_object_from_key(code)

    def get_highest_rate_from_airport_codes(self, airp_code_list, airp_dict, currency_dict):
        """For a given list of airports, it finds the maximum currency rate among countries linked to these airports"""
        rates = []
        for code in airp_code_list:
            rates.append(self.get_rate_from_country(code, airp_dict,currency_dict))
        return max(rates)

    def get_cheapest_rate_from_airport_codes(self, airp_code_list, airp_dict, currency_dict):
        """Like the above method but in this case it will find the minimum rate"""
        rates = []
        for code in airp_code_list:
            rates.append(self.get_rate_from_country(code, airp_dict, currency_dict))
        return min(rates)