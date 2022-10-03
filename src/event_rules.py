"""Class for changing an event's color base on it's content"""
from dataclasses import replace
from datetime import datetime
from typing import List, Optional

from src.event import Event
from src.event_colors import EventColor


class Condition:
    """Represents a condition an event can verify or not.
    Independent of any event at the beginning.
    Can be later evaluated with an event instance and returns a boolean.

    Ex: `
    condition = Condition().field('title').contains("Meeting")

    if condition.evaluate(event):
        ...
    `
    """

    def __init__(self):
        self.field_name = None
        self.evaluate_function = None

    def field(self, field: str):
        """Sets the event attribute on which the evaluate function will work on.
        `
        Condition().field('description')
        `
        Doesn't raise.

        """

        self.field_name = field
        return self

    def always(self):
        """Sets the condition to evaluate to True all the time"""
        self.evaluate_function = lambda event: True

    def contains(self, substring: str, *, case_sensitive=True):
        """Sets the condition to evaluate to True if :
        - case_sensitive is False and the provided field contains [substring] without taking letter case in consideration
        - case_sensitive is True and the provided field contains [substring] in the same case
        - .
        The event's field should be of type str. Raises TypeError if not."""
        self._check_str_type()

        def evaluate(event: Event) -> bool:
            try:
                value = event.get_attr_from_str(self.field_name)
            except AttributeError:
                return False
            if value is None:
                return False
            value: str
            if case_sensitive:
                return substring in value
            else:
                return substring.lower() in value.lower()

        self.evaluate_function = evaluate
        return self

    def equals(self, string: str):
        """Sets the condition to evaluate to True if the provided field is equals to the provided substring.
                The event's field should be of type str. Raises TypeError if not."""
        self._check_str_type()

        def evaluate(event: Event) -> bool:
            try:
                value = event.get_attr_from_str(self.field_name)
            except AttributeError:
                return False
            return value is not None and value == string

        self.evaluate_function = evaluate
        return self

    def starts_with(self, start_string: str):
        """Sets the condition to evaluate to True if the provided field starts with the provided substring.
                        The event's field should be of type str. Raises TypeError if not."""
        self._check_str_type()

        def evaluate(event: Event) -> bool:
            try:
                value: str = event.get_attr_from_str(self.field_name)

            except AttributeError:
                return False
            return value is not None and value.startswith(start_string)

        self.evaluate_function = evaluate

        return self

    def ends_with(self, end_string: str):
        """Sets the condition to evaluate to True if the provided field ends with the provided substring.
                        The event's field should be of type str. Raises TypeError if not."""
        self._check_str_type()

        def evaluate(event: Event) -> bool:
            try:
                value: str = event.get_attr_from_str(self.field_name)

            except AttributeError:
                return False
            return value is not None and value.endswith(end_string)

        self.evaluate_function = evaluate

        return self

    def logical_or(self, condition_1: 'Condition', condition_2: 'Condition'):
        def evaluate(event: Event) -> bool:
            return condition_1.evaluate(event) or condition_2.evaluate(event)
        self.evaluate_function = evaluate
        return self

    def evaluate(self, event: Event) -> bool:
        if not isinstance(event, Event):
            raise TypeError("event should me Event type")
        if self.evaluate_function is None:
            raise ValueError("Tried to evaluate a rule on a non initialized Condition.")
        return self.evaluate_function(event)

    def _check_str_type(self):
        if Event.type_of_field(self.field_name) is not str:
            raise TypeError(
                f"{Condition.contains} can only be called on a string field. {self.field=} {type(self.field)=}.")

    # todo : add negation, and


class Rule:
    """Represents a rule, independent of any event.
    The rule can be then applied to an event instance, and the chosen action(s) will be executed
    on the event only if it satisfies all the conditions.

    Ex :

    condition = Condition().field('description').contains('Important')
    rule = Rule().change_color(EventColor.TOMATO).on([condition])

    ...

    rule.apply_to_event(normal_event)
    assert(normal_event.color == None)
    rule.apply_to_event(important_event)
    assert(important_event.color == EventColor.TOMATO)

    """

    def __init__(self):
        self.apply_functions = []
        self.conditions = None

    def on(self, conditions: List[Condition]):
        if isinstance(conditions, Condition):
            self.conditions = [conditions]
        else:
            self.conditions = conditions
        return self

    def change_color(self, color: EventColor):
        def apply(event: Event) -> Event:
            return replace(event, color=color)

        self.apply_functions.append(apply)
        return self

    def prefix_str_to_field(self, field_name: str, append_value):
        """Will append a string before the provided field of the event.

        Ex:
        Rule().prefix_str_to_field('title', 'Doctor Appointment - ').on(Condition().field('title').contains('Mr. BOBO'))
        """
        def apply(event: Event) -> Event:
            field_value = event.get_attr_from_str(field_name)
            return replace(event, **{field_name:append_value + field_value})

        self.apply_functions.append(apply)
        return self

    def append_str_to_field(self, field_name: str, append_value):
        """Will append a string after the provided field of the event.

        Ex:
        Rule().append_str_to_field('title', ' - Doctor Appointment').on(Condition().field('title').contains('Mr. BOBO'))
        """

        def apply(event: Event) -> Event:
            field_value = event.get_attr_from_str(field_name)
            return replace(event, **{field_name:field_value + append_value})
            # copy = replace(event)
            # copy.__setattr__(field_name, field_value + append_value)
            # return copy

        self.apply_functions.append(apply)
        return self

    def set_field_str(self, field_name: str, value: str):
        """Will set a string field to the provided value

        Ex:
        Rule().set_field_str('title', 'Algebra').on(Condition().field('title').contains('HAX301'))
         """

        def apply(event: Event) -> Event:
            return replace(event,**{field_name:value})
            # copy.__setattr__(field_name, value)
            # return copy

        self.apply_functions.append(apply)
        return self

    def remove_event(self):
        """The event will be set to None after applying this rule.
        Also all the previous actions will be override.
        """

        def apply(e: Event) -> None:
            print(f'deleting event : {e.title}')
            return None

        self.apply_functions.append(apply)
        return self

    def apply_to_event(self, event: Event) -> Optional[Event]:
        """Checks if all conditions evaluate to True with this event, and returns the event, eventually modified with
        the current apply functions."""

        if not self.conditions:
            raise ValueError("No conditions provided.")

        event_copy = replace(event)

        if all((condition.evaluate(event_copy) for condition in self.conditions)):
            for func in self.apply_functions:
                if event_copy is None:
                    return None
                event_copy = func(event_copy)
        return event_copy

