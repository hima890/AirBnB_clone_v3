#!/usr/bin/python3
"""
Parse value to Create classes
"""

def parse_value(value):
        """
        Parses a value from the <key>=<value> syntax and converts
        it to the appropriate type (str, float, int).
        """
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1].replace('_', ' ').replace('\\"', '"')
            return value
        try:
            if '.' in value:
                return float(value)
            return int(value)
        except ValueError:
            return None
