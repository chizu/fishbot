#!/usr/bin/env python
"""Track karma for stuff."""
import backend

class Karma(backend.DatabaseObject):
	"""Class for tracking karma."""
	string = str()
	score = 0
	nick = str()

def karma(self, event):
	import re, fishapi
	before, string, operator = re.search(expression[0], event.arguments).groups()
	string = string.strip().lower()
	item = Karma(string=string, nick=event.source)
	if operator[0] == '+':
		if item.score < 7 - len(operator):
			item.score += len(operator) - 1
		else:
			item.score = 5
	elif operator[0] == '-':
		if item.score > -7 + len(operator):
			item.score -= len(operator) - 1
		else:
			item.score = -5
	else:
		print "karma.py: Something odd has happened."

expression = ("(^.*[^\w' +-]|^)(.*?)([+]{2,6}|[-]{2,6})", karma)
