#!/usr/bin/env python
"""!karma - Show karma stats for things.
!karma <thing> | stats"""
import backend, fishapi
from plugins.karma import Karma

def bang(pipein, arguments, event):
    token = arguments.strip().lower()
    if not token:
        token = fishapi.getnick(event.source()).strip().lower()
    if token == 'stats':
        all_karma = [(x.score, x.string) for x in Karma(-1)]
        large = max(all_karma)
        small = min(all_karma)
        return ("Highest score: %s (%s) - Lowest score: %s (%s)" % (large[0], large[1], small[0], small[1]), None)
    else:
        thing = Karma(-1, string=token)
        if thing:
            return ("'%s' has a score of: %s" % (arguments, thing.score), None)
        else:
            return ("'%s' has neutral karma." % (arguments), None)
