#!/usr/bin/python
def handle_say(self, source, to, message):
    respond = self.respond_to(source, to)
    self.say(respond, "eggs")
    self.say(respond, "beans")
    self.say(respond, "five")
    self.say(respond, "dentifrice")
    self.say(respond, "macho nachos")
    self.say(respond, "jam")
