#!/usr/bin/python
import os,re

def handle_say(self, source, to, message):
    respond = self.respond_to(source, to)
    if len(message.split(' ')) >= 2:
        fortune_dictionary = message.split(' ')[1]
    else:
        fortune_dictionary = ""
    for each in os.popen('fortune -n 500 -s %s' % re.escape(fortune_dictionary)).readlines():
	self.say(respond, each)
