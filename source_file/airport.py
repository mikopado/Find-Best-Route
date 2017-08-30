class Airport:
    def __init__(self, code, name, country, city, lat, long):
        try:
            self._code = code
            self._name = name
            self._country = country
            self._city = city
            self._latitude = lat
            self._longitude = long
        except AttributeError:
            self._code = ''
            self._name = ''
            self._country = ''
            self._city = ''
            self._latitude = 0.0
            self._longitude = 0.0

    def __setattr__(self, name, value): #Useful in case application allows user to pick a csv file for collecting data.
        # Prevents imported files not formatted as airport.csv file
        if name == '_latitude' or name == '_longitude':
            try:
                self.__dict__[name] = float(value)
            except ValueError:
                raise AttributeError
        elif name == '_name' or name == '_city' or name == '_country' or name == '_code':
            try:
                self.__dict__[name] = int(value)
            except ValueError:
                self.__dict__[name] = value
            else:
                raise AttributeError

    def get_code(self):
        return self._code

    def get_name(self):
        return self._name

    def get_country(self):
        return self._country

    def get_latitude(self):
        return self._latitude

    def get_longitude(self):
        return self._longitude

    def get_city(self):
        return self._city

    def __str__(self):
        return "{0:s} - {1:s}, {2:s}".format(self.get_code(), self.get_city(), self.get_country())

