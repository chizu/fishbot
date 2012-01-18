#!/usr/bin/python
"""The one that started it all ;_;"""
def cowsgomoo(self, event):
    event.server.say(self.respond_to(event.source, event.target), "LIEZ FISH GO MOO!")

expression = ("(?=(.*cow.*))(?=(.*go.*))(?=(.*moo.*))", cowsgomoo)
