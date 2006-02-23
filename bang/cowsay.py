#!/usr/bin/python
import re,os

def handle_say(self, source, to, message):
    respond = self.respond_to(source, to)
    cowsay = re.search('^!cowsay (.*)$', message)
    if cowsay:
	cowsay = cowsay.group(1)
	#for each in os.popen('cowsay ' + re.sub('\\\ ', ' ', re.escape(cowsay))):
	for each in os.popen('cowsay ' + re.sub('\-f', '', re.escape(cowsay))):
	    self.say(respond, (each or ("Cowsay command is missing.")))
