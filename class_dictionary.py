import csv
from custom_exceptions import *


class ClassDictionary:

    def __init__(self,csv_file):
        self.data_dict = {}
        self.load_data(csv_file)

    def load_data(self, csv_file):
        raise NotImplementedError("This is an abstract class cannot be instantiated")

    def get_object_from_key(self, key):
        if key in self.data_dict.keys():
            return self.data_dict[key]
        else:
            raise InvalidCodeError((key, ' is not a valid code!'))

    def open_csv_file(self, csv_file):
        '''Open csv file and return a tuple with open file and a dictionary containing all ther rows in the file.
        As for each csv file the process to open file is the same, this method is unique for all load_data methods
        in any classes (reusability). The method returns a tuple only for the purpose of closing the file after using
        it in the load_data methods, otherwise it couldn't be closed.'''
        try:
            file = open(csv_file, newline='', encoding='utf8')
            records = csv.DictReader(file)
        except UnicodeDecodeError:
            if not file.closed:
                file.close()
            raise FileFormatError("File is not in correct format! Must be CSV file")
        else:
            return file, records

