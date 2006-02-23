#!/usr/bin/python
import re,os

def handle_say(self, source, to, message):
    respond = self.respond_to(source, to)
    morse = re.search('^!morse (.*)$', message)
    if morse:
	morse = morse.group(1)
	for each in os.popen('echo "%s" | cwtext' % re.escape(morse)):
	    self.say(respond, (each))
