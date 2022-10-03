class InvalidUrlError(Exception):
    pass
class InvalidStatusCodeError(Exception):
    pass

class NoInternetConnectionError(Exception):
    pass

class UnkownRequestError(Exception):
    """Raised when an unknown error is thrown when making a get request"""
    pass

class CalendarNotAvailableError(Exception):
    """Raised when the server cannot provide the ics file.
    Example : The server is in maintenance."""
