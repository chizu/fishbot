#!/usr/bin/python
def handle_say(self, source, to, message):
    respond = self.respond_to(source, to)
    self.action(respond, "begins begins to glow with power, and gains 20 strength and 10 will.")
