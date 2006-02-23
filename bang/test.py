#!/usr/bin/python
def handle_say(self, source, to, message):
    respond = self.respond_to(source, to)
    self.say(respond, "This was a successful test.")
