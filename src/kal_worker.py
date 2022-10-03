from dataclasses import replace
from datetime import datetime
from os import remove
from typing import List
from copy import deepcopy


from src.cal_setup import get_calendar_service
from src.event import Event
from src.event_rules import Rule
from src.source_calendar.events_repository import EventsRepository
from src.google_calendar_handler import GoogleCalendarHandler
from src.mirror import Mirror
import pytz
import logging

from src.source_calendar.ics_calendar_provider import NetworkEventsProvider


class KalWorker:

    def __init__(self, source_ics_calendar_url : str, google_calendar_id: str,rules : List[Rule]):
        self.source_ics_calendar_url = source_ics_calendar_url
        self.google_calendar_id = google_calendar_id
        self.rules = rules

    def run(self, service):
        """
        - deletes all the events of the google_calendar starting from now, that have been created by Kal.
          (User created events should not be deleted.)
        - fetches the source_calendar
        - parses all the events
        - apply the rules to the events
        - upload all the new events to the google calendar
        
        """
        print(f"Running on google calendar : {self.google_calendar_id}, with {len(self.rules)}")
        handler = GoogleCalendarHandler(calendar_id=self.google_calendar_id,
                                        service=service)

        # Delete events after this date
        separation_date = datetime.now()

        google_events = handler.get_events_since_date(separation_date)

        google_kal_events = [e for e in google_events if self._event_has_kal_signature(e)]

        handler.delete_events_after_date(google_kal_events, separation_date)

        print(f"Deleted {len(google_kal_events)} events after {separation_date}")


        provider = NetworkEventsProvider(calendar_url=self.source_ics_calendar_url)
        repo = EventsRepository(provider)
        fresh_events = list(repo.get_events())

        new_events = [event for event in fresh_events if
                      event.start.astimezone(pytz.utc) > separation_date.astimezone(pytz.utc)]


        events_after_rules = get_events_after_applying_rules(new_events, self.rules)

        new_events_with_kal_signature = list(map(self._add_kal_signature, events_after_rules))

        handler.insert_events(new_events_with_kal_signature)
        print(f"Added: {len(events_after_rules)} events")


    def _add_kal_signature(self, event:Event)-> Event:
        """Ads a kal signature to event.
        A kal signature is a private property (https://developers.google.com/calendar/api/guides/extended-properties)
        indicating that this event has been created by the Kal service. 
        """
        properties = deepcopy(event.extended_properties)
        if properties is None:
            properties = dict()
        if 'private' not in properties:
            properties['private'] = {'kal': 'true'}
        else:
            properties['private']['kal'] = 'true'
        return replace(event, extended_properties=properties)

    def _event_has_kal_signature(self, event: Event)-> bool:
        """Checks if event has been "kal-signed". This is indicated that this event has been created by kal, 
        and thus is safe to delete."""
        properties = event.extended_properties
        if properties is None:
            return False
        if 'private' not in properties:
            return False
        private = properties['private']
        return 'kal' in private



def get_events_after_applying_rules(events:List[Event], rules: List[Rule]) -> List[Event]:
    """Applys all the rules provided to all the events. If an event becomes None after a rule, it won't be included in the returned list"""
    new_events: List[Event]
    new_events = []
    for e in events:
        for rule in rules:
            if e is None:
                break
            e = rule.apply_to_event(e)
        if e is not None:
            new_events.append(e)
    return new_events



