#!/usr/bin/python
def cowsgomoo(self, event):
    self.say(self.respond_to(event.source(), event.target()), "LIEZ FISH GO MOO!")

expression = ("(?=(.*cows.*))(?=(.*go.*))(?=(.*moo.*))", cowsgomoo)
