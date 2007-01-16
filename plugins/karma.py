#!/usr/bin/env python
"""Track karma for stuff."""
import backend

class Karma(backend.DatabaseObject):
    """Class for tracking karma."""
    string = str()
    score = 0

def karma(self, event):
    import re, fishapi
    before, string, operator = re.search(expression[0], event.arguments()[0]).groups()
    string = string.strip().lower()
    if operator == '++':
        Karma(string=string).score += 1
    elif operator == '--':
        Karma(string=string).score -= 1
    else:
        print "karma.py: Something odd has happened."

expression = ("(^.*[^\w ]|^)(.*?)([+]{2}|[-]{2})", karma)
