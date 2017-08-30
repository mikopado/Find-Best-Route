class InvalidCodeError(KeyError):
    pass

class FileNotExistError(FileNotFoundError):
    pass

class FileFormatError(KeyError):
    pass

class RouteNotFoundError(ValueError):
    pass