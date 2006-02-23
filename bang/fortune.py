#!/usr/bin/python
import os

def handle_say(self, source, to, message):
    respond = self.respond_to(source, to)
    for each in os.popen('fortune').readlines():
	self.say(respond, each)
