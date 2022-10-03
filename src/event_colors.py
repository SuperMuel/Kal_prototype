from enum import Enum


class EventColor(Enum):
    """Represents the colors used in google calendar"""

    LAVENDER = '1'
    SAGE = '2'
    GRAPE = '3'
    TANGERINE = '4'
    BANANA = '5'
    FLAMINGO = "6"
    PEACOCK = '7'
    GRAPHITE = '8'
    BLUEBERRY = '9'
    BASIL = '10'
    TOMATO = '11'

    @staticmethod
    def from_color_id(color_id: str):
        if color_id == '1':
            return EventColor.LAVENDER
        if color_id == '2':
            return EventColor.SAGE
        if color_id == '3':
            return EventColor.GRAPE
        if color_id == '4':
            return EventColor.TANGERINE
        if color_id == '5':
            return EventColor.BANANA
        if color_id == '6':
            return EventColor.FLAMINGO
        if color_id == '7':
            return EventColor.PEACOCK
        if color_id == '8':
            return EventColor.GRAPHITE
        if color_id == '9':
            return EventColor.BLUEBERRY
        if color_id == '10':
            return EventColor.BASIL
        if color_id == '11':
            return EventColor.TOMATO

    def to_color_code(self):
        m = {
            '1': 'a4bdfc',
            '2': '7ae7bf',
            '3': 'dbadff',
            '4': 'ff887c',
            '5': 'fbd75b',
            '6': 'ffb878',
            '7': '46d6db',
            '8': 'e1e1e1',
            '9': '5484ed',
            '10': '51b749',
            '11': 'dc2127',
        }
        return m[self.value]
