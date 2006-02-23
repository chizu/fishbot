#!/usr/bin/python
import re,os

def handle_say(self, source, to, message):
    respond = self.respond_to(source, to)
    wtf = re.search('^!wtf (.*)$', message)
    if wtf:
	wtf = wtf.group(1)
	for each in os.popen('wtf ' + re.escape(wtf)):
	    self.say(respond, (each or ("Gee... I don't know what " + wtf + "means...")))
