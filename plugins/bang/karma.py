#!/usr/bin/env python
"""!karma - Show karma stats for things.
!karma <thing> | stats"""
import backend, fishapi
from plugins.karma import Karma

def calckarma(thing):
	pcount = 0
	positive = 0
	ncount = 0
	negative = 0
	for each in thing:
		score = each.score
		if score < 0:
			ncount += 1
			negative += abs(score)
		elif score > 0:
			pcount += 1
			positive += score
	return (positive * pcount) - (negative * ncount)

def bang(pipein, arguments, event):
	token = arguments.strip().lower()
	if not token:
		token = fishapi.getnick(event.source).strip().lower()
		arguments = token
	if token == 'stats':
		all_karma = [(x.score, x.string) for x in Karma(-1)]
		large = max(all_karma)
		small = min(all_karma)
		return ("Highest score: %s (%s) - Lowest score: %s (%s)" % (large[0], large[1], small[0], small[1]), None)
	else:
		thing = Karma(-1, string=token)
		score = calckarma(thing)
		if score:
			return ("'%s' has a score of: %s" % (arguments, score), None)
		else:
			return ("'%s' has neutral karma." % (arguments), None)
