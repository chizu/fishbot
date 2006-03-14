#!/usr/bin/python
import urllib,string,re

def handle_say(self, source, to, message):
    respond = self.respond_to(source, to)
    resource = urllib.urlopen("http://www.sloganizer.net/en/?slogan=%s" % string.join(message.split(' ')[1:], '%20'))
    page = resource.read()
    resource.close()
    slogan = re.search('<p class="slogan">.<b>(.*)</b>.</p>', page)
    if slogan:
	slogan = slogan.group(1)
	self.say(respond, slogan)
