#!/usr/bin/python
import re,sys

def getnick(s):
    n = s.find("!")
    if n > -1:
        return s[:n]
    else:
        return s

def handle_say(self, source, to, message):
    respond = self.respond_to(source, to)
    try:
	if len(message.split('/')) == 4:
	    pattern = message.split('/')[1]
	    repl = message.split('/')[2]
	    self.say(respond, "%s meant to say: %s" % (getnick(source), re.sub(pattern, repl, self.last[getnick(source)][0])))
    except:
	self.say(respond, "Invalid regular expression.")
	raise
