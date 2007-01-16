#!/usr/bin/env python
"""!karma - Show karma stats for things.
!karma <thing>"""
import backend
from plugins.karma import Karma

def bang(pipein, arguments, event):
    if arguments.strip() == 'stats':
        all_karma = [x.score, x.string for x in Karma(-1)]
        large = max(all_karma)
        small = min(all_karma)
        return "Highest score: %s (%s) - Lowest score: %s (%s)" % (large.string, large.score, small.string, small.score)
    else:
        thing = Karma(-1, string=arguments)
        if thing:
            return ("'%s' has a score of: %s" % (arguments, thing.score), None)