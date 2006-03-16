#!/usr/bin/python
import string
import plugins.bang

def handle_say(self, source, to, message):
    respond = self.respond_to(source, to)
    self.say(respond, self.version + ". Available commands are: !" + string.join(plugins.bang.__all__,', !') + ".")
