#!/usr/bin/python
import re,os,random

def handle_say(self, source, to, message):
    respond = self.respond_to(source, to)
    choose = re.search('^!choose (.*)$', message)
    if choose:
	self.say(respond, "Entropy decides: " + random.choice(choose.group(1).split(',')))
