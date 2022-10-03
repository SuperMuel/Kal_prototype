import unittest
from datetime import datetime

from src.event import Event
from src.event_colors import EventColor
from src.event_rules import Condition

full_event = Event(title="Annual meeting", description="Sales report", location="San Francisco", start=datetime.now(),
                   end=datetime.now(), html_link="http://google.com", is_all_day=True, updated=datetime.now(),
                   id="oifezifuroijzfr", color=EventColor.TOMATO)


class TestConditions(unittest.TestCase):
    def test_contains(self):
        event = Event(title="Annual meeting", description="Sales report", location="San Francisco")
        condition = Condition().field('title').contains('ual mee')
        self.assertTrue(condition.evaluate(event))
        condition = Condition().field('description').contains('ual mee')
        self.assertFalse(condition.evaluate(event))
        condition = Condition().field('description').contains('repor')
        self.assertTrue(condition.evaluate(event))
        condition = Condition().field('location').contains('Franc')
        self.assertTrue(condition.evaluate(event))

    def test_equals(self):
        event = Event(title="Annual meeting", description="Sales report", location="San Francisco")
        condition = Condition().field('title').equals("Annual meeting")
        self.assertTrue(condition.evaluate(event))
        condition = Condition().field('description').equals("Sales report")
        self.assertTrue(condition.evaluate(event))
        condition = Condition().field('location').equals("San Francisco")
        self.assertTrue(condition.evaluate(event))

        condition = Condition().field('title').equals("fezoing")
        self.assertFalse(condition.evaluate(event))
        condition = Condition().field('description').equals("Sale report")
        self.assertFalse(condition.evaluate(event))
        condition = Condition().field('location').equals("Moncuq")
        self.assertFalse(condition.evaluate(event))

    def test_starts_with(self):
        event = Event(title="Annual meeting", description="Sales report", location="San Francisco")
        condition = Condition().field('title').starts_with("Annual")
        self.assertTrue(condition.evaluate(event))
        condition = Condition().field('description').starts_with("Sales ")
        self.assertTrue(condition.evaluate(event))
        condition = Condition().field('location').starts_with("Sa")
        self.assertTrue(condition.evaluate(event))

        condition = Condition().field('title').starts_with("AAnnual")
        self.assertFalse(condition.evaluate(event))
        condition = Condition().field('description').starts_with("Saless")
        self.assertFalse(condition.evaluate(event))
        condition = Condition().field('location').starts_with("K")
        self.assertFalse(condition.evaluate(event))

    def test_ends_with(self):
        event = Event(title="Annual meeting", description="Sales report", location="San Francisco")
        condition = Condition().field('title').ends_with("ing")
        self.assertTrue(condition.evaluate(event))
        condition = Condition().field('description').ends_with("report")
        self.assertTrue(condition.evaluate(event))
        condition = Condition().field('location').ends_with("")
        self.assertTrue(condition.evaluate(event))

        condition = Condition().field('title').ends_with("f")
        self.assertFalse(condition.evaluate(event))
        condition = Condition().field('description').ends_with("the brown fox jumps over the frog")
        self.assertFalse(condition.evaluate(event))
        condition = Condition().field('location').ends_with(".")
        self.assertFalse(condition.evaluate(event))

    def test_none_fields(self):
        """Conditions on none fields should evaluate to False"""

        event = Event()

        condition = Condition().field('title').contains('ual mee')
        self.assertFalse(condition.evaluate(event))
        condition = Condition().field('description').contains('repor')
        self.assertFalse(condition.evaluate(event))
        condition = Condition().field('location').contains('Franc')
        self.assertFalse(condition.evaluate(event))

        condition = Condition().field('title').equals("Annual meeting")
        self.assertFalse(condition.evaluate(event))
        condition = Condition().field('description').equals("Sales report")
        self.assertFalse(condition.evaluate(event))
        condition = Condition().field('location').equals("San Francisco")
        self.assertFalse(condition.evaluate(event))

        condition = Condition().field('title').starts_with("Annual")
        self.assertFalse(condition.evaluate(event))
        condition = Condition().field('description').starts_with("Sales ")
        self.assertFalse(condition.evaluate(event))
        condition = Condition().field('location').starts_with("Sa")
        self.assertFalse(condition.evaluate(event))

        condition = Condition().field('title').ends_with("ing")
        self.assertFalse(condition.evaluate(event))
        condition = Condition().field('description').ends_with("report")
        self.assertFalse(condition.evaluate(event))
        condition = Condition().field('location').ends_with("")
        self.assertFalse(condition.evaluate(event))

    def test_condition_not_set_raises_ValueError(self):
        """Evaluating a condition on a event while not having set any condition should raise ValueError"""
        event = Event(title="Annual meeting", description="Sales report", location="San Francisco")
        condition = Condition()
        self.assertRaises(ValueError, lambda: condition.evaluate(event))
        condition = Condition().field("title")
        self.assertRaises(ValueError, lambda: condition.evaluate(event))
        condition = Condition().field("non existing")
        self.assertRaises(ValueError, lambda: condition.evaluate(event))

    def test_invalid_field(self):
        """Conditions that try to access an non existing event property should raise AttributeError"""
        event = Event(title="Annual meeting", description="Sales report", location="San Francisco")
        self.assertRaises(AttributeError, lambda: Condition().field("invalid").contains("something"))

    def test_str_conditions_on_no_str_fields(self):
        """Using 'contains', 'startswith', ... methods on no-str fields should raise TypeError"""
        for field in ('start', 'end', 'updated', 'color'):
            for method in ('contains', 'starts_with', 'ends_with', 'equals'):
                self.assertRaises(TypeError, lambda: Condition().field(field).__getattribute__(method)("2021"))
