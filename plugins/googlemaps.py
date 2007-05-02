#!/usr/bin/python
def cowsgomoo(self, event):
    event.server.say(self.respond_to(event.source, event.target), "<toshi>GoOgLe MaPs!?!?</toshi>")

expression = ("(?=(.*google.*))(?=(.*map.*))", cowsgomoo)
