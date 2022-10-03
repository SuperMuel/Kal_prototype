from src.source_calendar.ics_calendar_provider import CalendarProvider
from src.event import Event

from typing import Iterator


class EventsRepository:
    """Parses events from an Calendar object and returns an iterator of events."""

    def get_events(self) -> Iterator[Event]:
        calendar = self.provider.get_calendar()

        for event in calendar.events:
            yield Event(
                title=event.name,
                description=event.description,
                location=event.location,
                start=event.begin.datetime,
                end=event.end.datetime,
                html_link=event.url,
                is_all_day=event.all_day,
                created=event.created,
                updated=event.last_modified,
            )

    def __init__(self, provider: CalendarProvider):
        self.provider = provider
