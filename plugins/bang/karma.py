#!/usr/bin/env python
"""!karma - Show karma stats for things.
!karma <thing>"""
import backend
from plugins.karma import Karma

def bang(pipein, arguments, event):
    thing = Karma(-1, string=arguments)
    if thing:
        return ("'%s' has a score of: %s" % (arguments, thing.score), None)
