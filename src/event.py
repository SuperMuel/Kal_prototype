from dataclasses import dataclass, replace
from datetime import datetime
from typing import Any, Optional

import pytz

from src.event_colors import EventColor


@dataclass(frozen=True)
class Event:
    id: str = None
    title: str = None
    description: str = None
    location: str = None
    html_link: str = None
    is_all_day: bool = False
    created: datetime = None
    updated: datetime = None
    start: datetime = None
    end: datetime = None
    color: EventColor = None
    extended_properties: Optional[dict] = None



    @staticmethod
    def type_of_field(field: str) -> type:
        """Returns what type a field should be.
        :raises AttributeError if field is not valid"""


        field = Event._format_field_name(field)

        if field in ('id', 'title', 'description', 'location', 'html_link'):
            return str
        if field in ('created', 'updated', 'start', 'end'):
            return datetime
        if field in ('is_all_day'):
            return bool
        if field == 'color':
            return EventColor
        raise AttributeError(f'Unknown field name : {field}')

    @staticmethod
    def _format_field_name(field: str) -> str:
        field = field.lower()
        if field == 'summary':
            field = 'title'
        elif field == 'begin':
            field = 'start'
        elif field == 'url':
            field = 'html_link'
        return field

    def get_attr_from_str(self, attr: str) -> Any:
        return self.__getattribute__(self._format_field_name(attr))

    def __lt__(self, other) -> bool:
        """Allows sorting by start date."""
        return self.starts_before(other)

    def ends_before(self, other, strict=True) -> bool:
        if not strict:
            return self.compare_end_time(other) <= 0

        return self.compare_end_time(other) < 0

    def ends_after(self, other, strict=True) -> bool:
        if not strict:
            return self.compare_end_time(other) >= 0
        return self.compare_end_time(other) > 0

    def starts_before(self, other, strict=True) -> bool:
        if not strict:
            return self.compare_start_time(other) <= 0
        return self.compare_start_time(other) < 0

    def starts_after(self, other, strict=True) -> bool:
        if not strict:
            return self.compare_start_time(other) >= 0
        return self.compare_start_time(other) > 0

    def starts_at_the_same_time(self, other, precision=0) -> bool:
        """Two events starts at the same time if the absolute number of seconds that separate them
        is less than 'precision = 0'."""
        return abs(self.compare_start_time(other)) <= precision

    def compare_start_time(self, other):
        """:returns the time in seconds that separates two event beginnings.
        =0 if beginnings are the same.
        < 0 if self starts before other
        > 0 if self starts after other
        """

        if isinstance(other, Event):
            if self.start is None or other.start is None:
                raise ValueError("Cannot compare none values")
            return (self.start.astimezone(pytz.utc) - other.start.astimezone(pytz.utc)).total_seconds()
        elif isinstance(other, datetime):
            return (self.start.astimezone(pytz.utc) - other.astimezone(pytz.utc)).total_seconds()
        raise TypeError("Other should be Event type")

    def compare_end_time(self, other):
        """:returns the time in seconds that separates two event beginnings.
                =0 if beginnings are the same.
                < 0 if self ends before other
                > 0 if self ends after other
                """
        if isinstance(other, Event):
            if self.end is None or other.end is None:
                raise ValueError("Cannot compare none values")
            return (self.end.astimezone(pytz.utc) - other.end.astimezone(pytz.utc)).total_seconds()
        elif isinstance(other, datetime):
            return (self.end.astimezone(pytz.utc) - other.astimezone(pytz.utc)).total_seconds()
        raise TypeError("Other should be Event type")
