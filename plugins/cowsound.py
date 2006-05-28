#!/usr/bin/python
def cowsound(self, event):
    self.say(self.respond_to(event.source(), event.target()), "FISH GO MOO!")

expression = ("(?=(.*what.*))(?=(.*sound.*))(?=(.*cow.*))", cowsound)
