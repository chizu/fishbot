#!/usr/bin/python
import string

def handle_say(self, source, to, message):
    respond = self.respond_to(source, to)
    self.say(respond, "Fishbot 2.0, now with runtime dynamic ! commands. Available commands are: !" + string.join(self.bang_commands.keys(),', !') + ".")
