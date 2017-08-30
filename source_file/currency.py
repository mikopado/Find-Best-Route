class Currency:

    def __init__(self, code, name, country):
        self._code = code
        self._name = name
        self._country = country

    def get_name(self):
        return self._name

    def get_code(self):
        return self._code

    def get_country(self):
        return self._country

    def __str__(self):
        return '%s - %s' % (self.get_code(), self.get_country())
