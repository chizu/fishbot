#!/usr/bin/python
def cowsound(self, event):
    self.say(self.respond_to(event.source, event.target), "COWS ANTI-MOO!")

expression = ("(?=(.*what.*))(?=(.*sound.*))(?=(.*cow.*))", cowsound)
