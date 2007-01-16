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
    count = 0
    for each in backend.last(event.source(),25):
        if string + operator in each[4]:
            count++
    if count > 5:
        Karma(string=fishapi.getnick(event.source())).score -= 50
        return
    if operator == '++':
        Karma(string=string).score += 1
    elif operator == '--':
        Karma(string=string).score -= 1
    else:
        print "karma.py: Something odd has happened."

expression = ("(^.*[^\w ]|^)(.*?)([+]{2}|[-]{2})", karma)
