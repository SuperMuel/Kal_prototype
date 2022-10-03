import unittest

from src.event import Event
from datetime import datetime

normal_event = Event(start=datetime(2021, 9, 13, 9), end=datetime(2021, 9, 13, 10))

before = Event(start=datetime(2021, 8,8, 10), end=datetime(2021, 9, 9, 11))

after = Event(start=datetime(2022, 7,8, 10), end=datetime(2022, 10, 9, 11))

old_date = datetime(1999, 10, 19)

class EventTest(unittest.TestCase):
    def test_compare_time_errors(self):
        """Tests if right exceptions are raised."""


        self.assertRaises(ValueError, lambda: Event().compare_start_time(normal_event))
        self.assertRaises(TypeError, lambda: normal_event.compare_start_time(1))

        self.assertRaises(ValueError, lambda: Event().compare_end_time(normal_event))  # event has no end date
        self.assertRaises(TypeError, lambda: normal_event.compare_end_time(1))  # invalid type for other object


    def test_event_starts_after(self):
        self.assertTrue(after.starts_after(before))
        self.assertTrue(before.starts_after(old_date))

    def test_event_starts_before(self):
        self.assertTrue(before.starts_before(after))
        self.assertFalse(after.starts_before(old_date))

    def test_event_compares_not_strict(self):
        self.assertTrue(normal_event.starts_before(normal_event, strict=False))
        self.assertTrue(normal_event.starts_after(normal_event, strict=False))
        self.assertTrue(normal_event.ends_before(normal_event, strict=False))
        self.assertTrue(normal_event.ends_after(normal_event, strict=False))

    def test_lt(self):
        self.assertTrue(before< after)
    # def test_compare_time(self):
    #
    #
    #     before = datetime(2021, 9, 13, )
    #
    #
    #     after = Event(start=)
