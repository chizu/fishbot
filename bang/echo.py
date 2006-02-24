#!/usr/bin/python
import re,os

def handle_say(self, source, to, message):
    respond = self.respond_to(source, to)
    arg = re.search('^!echo (.*)$', message)
    if hasattr(arg, 'group'):
	arg = arg.group(1)
    self.say(respond, (arg or "Mooo"))
