import unittest
from datetime import datetime

from src.event import Event
from src.event_colors import EventColor
from src.event_rules import Condition, Rule

event_no_color = Event(
    title="HAX301X",
    description="L2 CUPGE\nL2 Maths\Double L2 Info Maths(portée par info)\nAlgèbre III Réduction des endomorphismes\nA valider\nBABENKO IVAN\n(Exporté le:16/09/2021 14:36)",
    location="Amphi 5.02",
    start=datetime(2021, 9, 17, 13, 15),
    end=datetime(2021, 9, 17, 14, 45),

)

condition_true = Condition().field('title').contains("301")
condition_true2 = Condition().field('description').contains("Double L2")
condition_false = Condition().field('description').contains("fjeoijzfoj foij rpoij")


class TestRules(unittest.TestCase):

    def test_one_condition_true(self):
        rule = Rule().change_color(EventColor.BASIL).on([condition_true])
        rule.apply_to_event(event_no_color)
        self.assertEqual(event_no_color.color, EventColor.BASIL)
        event_no_color.color = None

    def test_two_conditions_true(self):
        rule = Rule().change_color(EventColor.TOMATO).on([condition_true, condition_true2])
        rule.apply_to_event(event_no_color)
        self.assertEqual(event_no_color.color, EventColor.TOMATO)
        event_no_color.color = None

    def test_one_condition_false(self):
        initial_color = event_no_color.color
        rule = Rule().change_color(EventColor.GRAPHITE).on([condition_false])
        rule.apply_to_event(event_no_color)
        self.assertEqual(initial_color, event_no_color.color)

    def test_one_true_one_false(self):
        initial_color = event_no_color.color
        rule = Rule().change_color(EventColor.GRAPHITE).on([condition_false, condition_true])
        rule.apply_to_event(event_no_color)
        self.assertEqual(initial_color, event_no_color.color)
