#!/usr/bin/python
import os,re

def handle_say(self, source, to, message):
    respond = self.respond_to(source, to)
    if len(message.split(' ')) >= 2:
        spelling = message.split(' ')[1:]
    else:
        result = self.backend.last(source, 2)
        spelling = [result[1][4]]
	print result
    for spell in spelling:
        for each in os.popen('echo %s | aspell -a' % re.escape(spell)).readlines():
            for each in each.split("\n"):
                if len(each) > 0 and each[0] == '&':
                    self.say(respond, each)
