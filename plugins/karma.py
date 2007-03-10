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
	if operator == '++':
		if item.score < 5:
			item.score += 1
	elif operator == '--':
		if item.score > -5:
			Karma(string=string).score -= 1
	else:
		print "karma.py: Something odd has happened."

expression = ("(^.*[^\w' ]|^)(.*?)([+]{2}|[-]{2})", karma)
