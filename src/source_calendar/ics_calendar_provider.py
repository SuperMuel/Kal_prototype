from abc import ABC, abstractmethod

import requests

from ics import Calendar

from src.exceptions import InvalidUrlError, InvalidStatusCodeError, NoInternetConnectionError, UnkownRequestError, \
    CalendarNotAvailableError
from src.util import is_url_valid, robust_request

import logging


class CalendarProvider(ABC):
    @abstractmethod
    def get_calendar(self) -> Calendar:
        """Returns a Calendar instance from the icspy module."""
        pass


class NetworkEventsProvider(CalendarProvider):
    calendar_url: str

    def __init__(self, calendar_url: str):
        if not is_url_valid(calendar_url):
            raise InvalidUrlError(calendar_url)
        self.calendar_url = calendar_url

    def get_calendar(self) -> Calendar:
        """Returns a Calendar object of the icspy module."""
        return Calendar(self._get_ics_file())

    def _get_ics_file(self) -> str:
        """Returns the string representing the content of an ics file.
        Raises NoInternetConnectionError, UnknownRequestError"""

        try:
            response = robust_request(self.calendar_url)
            if response.status_code != 200:
                raise InvalidStatusCodeError(f"The ics file request returned a {response.status_code} status code.")

            response = requests.get(self.calendar_url)
        except requests.ConnectionError as e:
            logging.error(f"Could not fetch ics file from internet. The connection is probably broken : {e}")
            raise NoInternetConnectionError()
        except Exception as e:
            logging.error(
                f"Could not fetch ics file from internet : {self.calendar_url}. Error : {type(e).__name__} {e}")
            raise UnkownRequestError()

        content_type = response.headers["Content-Type"]
        if "html" in content_type.lower():
            raise CalendarNotAvailableError(f"Content type is {content_type}")

        return response.text


class FileEventsProvider(CalendarProvider):
    def get_calendar(self) -> Calendar:
        with open(self.file_path, "r", encoding=self.encoding) as F:
            return Calendar(F.read())

    def __init__(self, file_path, encoding='utf-8'):
        self.file_path = file_path
        self.encoding = encoding
