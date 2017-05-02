from aircraft import Aircraft
from parent_class_dictionary import ParentClassDictionary
from custom_exceptions import *


class AircraftDictionaryParent(ParentClassDictionary):

    def __init__(self, csv_file):
        self.data_dict = {}
        ParentClassDictionary.__init__(self, csv_file)

    def load_data(self, csv_file):
        """Gets a tuple of open csv file and records of all data in it an then populated aircrafts dictionary.
        The method handles FileNotFoundError if the program tries to upload a file which doesn't exist and KeyError
        if program tries to upload a csv file which doesn't have the sam type of data and so the columns are not matching.
        For example if the program uploads currencyrates.csv it will raise a KeyError exception and it will be handled."""
        try:
            file, records = self.open_csv_file(csv_file)
            try:
                for row in records:
                    aircraft = Aircraft(row['model'], row['type'], row['manufacturer'],
                                        row['range'], row['max_fuel_capacity'])
                    self.data_dict[row['model']] = aircraft
            except KeyError:
                raise FileFormatError("Columns are not matching! Wrong file format")
            finally:
                file.close()

        except FileNotFoundError:
            raise FileNotExistError('File not exists')

    def get_list_aircrafts_model(self):
        """Retrieves the list of all aircrafts model from csv file. Need it for GUI"""
        list_aircrafts = []
        for i in self.data_dict.keys():
            list_aircrafts.append(i)
        return list_aircrafts