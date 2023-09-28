from dataclasses import dataclass
from datetime import datetime
from typing import List

import pytz
from googleapiclient.discovery import Resource

from src.event import Event
from src.event_colors import EventColor
from src.util import group_elements_by


@dataclass
class GoogleCalendarHandler:
    """Api for inserting, deleting events from a google calendar"""
    calendar_id: str
    service: Resource
    time_zone: str = "Europe/Paris"

    BATCH_MAX_REQUEST_NUMBER = 50

    @staticmethod
    def _parseEvent(response: dict) -> Event:
        # {'kind': 'calendar#event', 'etag': '"3263102242854000"', 'id': 'mt972eo82fsqaschfh1nkacpes', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=bXQ5NzJlbzgyZnNxYXNjaGZoMW5rYWNwZXMgdnMyZWhlcWJvdWZ2ZzYza2Rla2Y1bXVpMG9AZw', 'created': '2021-09-13T16:38:41.000Z', 'updated': '2021-09-13T16:38:41.427Z', 'summary': 'HAX301X', 'description': 'L2 CUPGE\nL2 Maths\nDouble L2 Info Maths (portée par info)\nAlgèbre III Réduction des endomorphismes\nA valider\nBABENKO   IVAN\n(Exporté le:13/09/2021 18:38)', 'location': 'Amphi 5.02', 'colorId': '1', 'creator': {'email': 'supermuel66@gmail.com'}, 'organizer': {'email': 'vs2eheqboufvg63kdekf5mui0o@group.calendar.google.com', 'displayName': 'L2', 'self': True}, 'start': {'dateTime': '2021-12-09T08:00:00+01:00', 'timeZone': 'Europe/Paris'}, 'end': {'dateTime': '2021-12-09T09:30:00+01:00', 'timeZone': 'Europe/Paris'}, 'iCalUID': 'mt972eo82fsqaschfh1nkacpes@google.com', 'sequence': 0, 'reminders': {'useDefault': True}, 'eventType': 'default'}

        # etag = response.get('etag', None)
        # kind = response.get('kind', None)
        # status = response.get('status', None)
        id = response.get('id', None)
        html_link = response.get('htmlLink', None)
        created = response.get('created', None)
        try:
            created = datetime.fromisoformat(created)
        except Exception as e:
            # print(e, type(e).__name__)
            created = None
        updated = response.get('updated', None)
        try:
            updated = datetime.fromisoformat(updated)
        except Exception:
            updated = None
        title = response.get('summary', None)
        description = response.get('description', None)
        location = response.get('location', None)
        color_id = response.get('colorId', None)
        color = None
        if color_id is not None:
            color = EventColor.from_color_id(color_id)

        is_all_day=False
        start_dict = response['start']
        if start_dict is not None:
            if 'dateTime' in start_dict:
                start_dt = datetime.fromisoformat(start_dict['dateTime'])
            elif 'date' in start_dict:
                is_all_day = True
                start_dt = datetime.strptime(start_dict['date'], '%Y-%m-%d')
            else:
                raise ValueError('Unknown date type')

        end_dict = response['end']
        if end_dict:
            if 'dateTime' in end_dict:
                end_dt = datetime.fromisoformat(end_dict['dateTime'])
            elif 'date' in end_dict:
                is_all_day = True
                end_dt = datetime.strptime(end_dict['date'], '%Y-%m-%d')
            else:
                raise ValueError('Unknown date type')
        


        extended_properties = response.get('extendedProperties', {})

        return Event(title=title,
                     description=description,
                     location=location,
                     start=start_dt,
                     end=end_dt,
                     color=color,
                     updated=updated,
                     created=created,
                     html_link=html_link,
                     id=id,
                     extended_properties = extended_properties,
                     is_all_day=is_all_day,
                     )

    def get_events_since_date(self, date: datetime = None, limit: int = None) -> List[Event]:
        """
        if the event has started but is not yet finished at date, it is included.
        if the event's end matches exactly the date, it is excluded.

        results are ordered by their start time. It's done on google servers, the method don't verify
        the order afterwards.
        """


        request = self.service.events().list(
            calendarId=self.calendar_id,
            timeMin=date.astimezone(pytz.utc).isoformat() if date else None,

            # Whether to expand recurring events into instances and only return single one-off events and instances of
            # recurring events, but not the underlying recurring events themselves.
            singleEvents=True,
            orderBy='startTime',
            maxResults=limit,
        )

        events_dicts = []

        while request is not None:
            response = request.execute()

            events_dicts += response.get('items', [])

            request = self.service.events().list_next(request, response)

        return list(map(GoogleCalendarHandler._parseEvent, events_dicts))

    def get_events(self, limit: int = None) -> List[Event]:
        return self.get_events_since_date(limit=limit)

    # def get_time_zone(self) -> str:
    #     return self.service.Calendars().execute()  # todo : parse and return timezone
    #     # todo : move this to an higher class

    def delete_events_after_date(self, events: List[Event], date: datetime = None):
        """Deletes all events that strictly start after `date`
        So it doesnt' delete an not-yet-finished event."""
        to_delete_ids = [event.id for event in events if event.start.astimezone(pytz.utc) > date.astimezone(pytz.utc)]
        self.delete_events(to_delete_ids)

    def delete_events(self, events_ids: List[str]):
        for event_ids_sublist in group_elements_by(GoogleCalendarHandler.BATCH_MAX_REQUEST_NUMBER, events_ids):
            batch = self.service.new_batch_http_request()
            for event_id in event_ids_sublist:
                batch.add(self.service.events().delete(calendarId=self.calendar_id, eventId=event_id))
            batch.execute()

    def insert_events(self, events: List[Event]) :
        """extended_properties:
        { # Extended properties of the event.
        "private": { # Properties that are private to the copy of the event that appears on this calendar.
          "a_key": "A String", # The name of the private property and the corresponding value.
        },
        "shared": { # Properties that are shared between copies of the event on other attendees' calendars.
          "a_key": "A String", # The name of the shared property and the corresponding value.
        }
        to set for all the events
        """


        for event_ids_sublist in group_elements_by(GoogleCalendarHandler.BATCH_MAX_REQUEST_NUMBER, events):
            batch = self.service.new_batch_http_request()
            for event in event_ids_sublist:
                batch.add(self.service.events().insert(
                    calendarId=self.calendar_id,
                    body=GoogleCalendarHandler._event_to_body(event),
                ))
            batch.execute()

    @staticmethod
    def _event_to_body(event: Event) -> dict:
        d = {
            'summary': event.title,
            'description': event.description,
            'start': {'dateTime': event.start.isoformat(),
                      'timeZone': "Europe/Paris"},
            'end': {'dateTime': event.end.isoformat(),
                    'timeZone': 'Europe/Paris'},
            'location': event.location,
            "extendedProperties": event.extended_properties

        }


        if event.color is not None:
            d['colorId'] = event.color.value
        return d

    def insert_events_after_date(self, events: List[Event], date: datetime, extended_properties:dict= None):
        """Inserts into the calendar all the events that start after date
        Throws ValueError if an event.end is None"""
        if any([event.end is None for event in events]):
            raise ValueError("C")
        to_insert_events = [event for event in events if event.end >= date]
        self.insert_events(to_insert_events)

    def get_calendars_list(self):
        """Returns json as a dict representing the calendars associated with the google account."""
        calendars = self.service.calendarList().list().execute()
        return calendars.get('items', [])

    def get_calendar_info(self, calendar_id):
        return self.service.calendarList().get(calendarId=calendar_id).execute()

    def insert_calendar(self, title: str, description: str, time_zone="Europe/Paris") -> str:
        """Create and insert a new calendar with the provided title and description. Returns the created calendar's id."""

        body = {
            "kind": "calendar#calendar",
            "description": description,
            "summary": title,
            "timeZone": time_zone
        }

        response = self.service.calendars().insert(body=body).execute()
        id = response['id']
        return id

