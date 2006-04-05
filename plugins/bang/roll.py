#!/usr/bin/python
import re,os,random

def handle_say(self, source, to, message):
    respond = self.respond_to(source, to)
    roll = re.search('^!roll (.*)$', message)
    if roll:
	roll = int(roll.group(1))
    else:
        roll = 20
    self.say(respond, str(random.randint(1,roll)))
        
