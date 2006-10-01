#!/usr/bin/python
import urllib,string,re

def handle_say(self, source, to, message):
    respond = self.respond_to(source, to)
    resource = urllib.urlopen("http://www.webweaving.org/")
    page = resource.read()
    resource.close()
    insult = re.search('(Thou\s[^\n]*)', page)
    if insult:
	insult = insult.group(1)
	self.say(respond, str(' '.join(message.split(' ')[1:])) + ', ' + insult + "!")
