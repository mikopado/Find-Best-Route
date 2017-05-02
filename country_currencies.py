from currency import Currency
from parent_class_dictionary import ParentClassDictionary
from custom_exceptions import *

class CountryCurrenciesDictionaryParent(ParentClassDictionary):

    def __init__(self, csv_file):
        self.data_dict = {}
        ParentClassDictionary.__init__(self, csv_file)

    def load_data(self, csv_file):
        try:
            file, records = self.open_csv_file(csv_file)
            try:
                for row in records:
                    currency = Currency(row['currency_alphabetic_code'], row['currency_name'],
                                        row['name'])
                    self.data_dict[row['name']] = currency
            except KeyError:
                raise FileFormatError("Columns are not matching! Wrong file format")
            finally:
                file.close()
        except FileNotFoundError:
            raise FileNotExistError('File not exists')


