import math
from airport import Airport
from class_dictionary import ClassDictionary
from custom_exceptions import *


class AirportAtlas(ClassDictionary):

    def __init__(self, csv_file):
        self.data_dict = {}
        ClassDictionary.__init__(self, csv_file)

    def load_data(self, csv_file):
        """The method has the same function of AircraftsDictionary.load_data. For reusability it would be appropriate making
        one method shared by all classes but it turns it out quite complicated to do it as method will need different
        parameters for each class (e.g. list of attributes to pass to instatiate the Airport, Aircraft, Currency object)"""
        try:
            file, records = self.open_csv_file(csv_file)
            try:
                for row in records:
                    airport = Airport(row['Code'], row['Airport Name'], row['Country'], row['City'],
                                      row['Latitude'],
                                      row['Longitude'])
                    self.data_dict.setdefault(row["Code"], airport)
            except KeyError:
                raise FileFormatError("Columns are not matching! Wrong file format")

            finally:
                file.close()
        except FileNotFoundError:
            raise FileNotExistError('File not exists')

    @staticmethod
    def distance_on_unit_sphere(lat1, long1, lat2, long2):
        """Great circle distance beetween two points on earth calculate using Haversine formula """
        to_radians = math.pi / 180.0
        radius = 6371
        lat1_rad = lat1 * to_radians
        lat2_rad = lat2 * to_radians
        delta_lat = (lat2 - lat1) * to_radians
        delta_long = (long2 - long1) * to_radians
        chord = math.sin(delta_lat/2) * math.sin(delta_lat/2) + math.cos(lat1_rad) * math.cos(lat2_rad) * \
                                                              math.sin(delta_long/2) * math.sin(delta_long/2)
        angular_dist = 2 * math.atan2(math.sqrt(chord), math.sqrt(1-chord))

        return int(radius * angular_dist)

    def get_distance_between_airports(self, airport_code1, airport_code2):
        airport_code1 = airport_code1.upper()
        airport_code2 = airport_code2.upper()
        if airport_code1 in self.data_dict.keys() and airport_code2 in self.data_dict.keys():

            return self.distance_on_unit_sphere(self.data_dict[airport_code1].get_latitude(),
                                                self.data_dict[airport_code1].get_longitude(),
                                                self.data_dict[airport_code2].get_latitude(),
                                                self.data_dict[airport_code2].get_longitude())
        else:
            raise InvalidCodeError("Code not valid")

    def get_airport_at_max_distance(self, home_airport, list_of_airport):
        """Given a list of airports and a selected airport, it will find the aiport in this list that it's at
        maximum distance from the selected airport"""
        output_dict = {}
        for airp in list_of_airport:
            distance = self.get_distance_between_airports(home_airport, airp)
            output_dict[distance] = airp
        max_distance = max(output_dict.keys())
        return output_dict[max_distance]

    def get_list_of_airports_from_country(self, country): #Need for GUI. Retrieves a list of all airport in a selected country
        list_codes = []
        for code in self.data_dict.keys():
            airp = self.get_object_from_key(code)
            if airp.get_country() == country:
                list_codes.append(code)
        return list_codes

    def get_list_countries(self): #Need for GUI. Get list of all countries in the airport.csv file
        list_countries = []
        for element in self.data_dict.keys():
            country = self.get_object_from_key(element).get_country()
            if country not in list_countries:
                list_countries.append(country)
        return list_countries