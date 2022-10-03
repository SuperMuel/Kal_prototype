from typing import List
from src.event_rules import Rule

class Mirror:
    """
    name: the mirror's custom name, for logging and credentials persistence. Use an alphanumeric format: [A-Za-z0-9] 
    source_ics_calendar_url: Url of the ics file
    google_calendar_id: Find it in the parameters of calendar.google.com on Desktop (see /images/find_google_calendar_id.png)
    rules: A list of custom rules
    """
    def __init__(self, title: str, source_ics_calendar_url: str, google_calendar_id: str, rules: List[Rule]):
        self.title = title
        self.source_ics_calendar_url = source_ics_calendar_url
        self.google_calendar_id = google_calendar_id
        self.rules = rules
