#!/usr/bin/python
def alot(self, event):
    event.server.say(self.respond_to(event.source, event.target), "The alot comes for you - http://i.imgur.com/g9KEx.png")

expression = (".*[Aa][Ll][Oo][Tt].*", alot)
