#!/usr/bin/python
import re,sys
import fishapi

def handle_say(self, source, to, message):
    respond = self.respond_to(source, to)
    try:
	if len(message.split('/')) == 4:
	    pattern = message.split('/')[1]
	    repl = message.split('/')[2]
	    self.say(respond, "%s meant to say: %s" % (self.getnick(source), re.sub(pattern, repl, fishapi.backend.last(source, 2)[1][4])))
    except:
	self.say(respond, "Invalid regular expression.")
	raise
