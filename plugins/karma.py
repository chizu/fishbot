#!/usr/bin/env python
"""Track karma for stuff."""
import re

from sqlalchemy import Column, Integer, String

from backend import DatabaseObject, get_session
from fishapi import getnick


class Karma(DatabaseObject):
	"""Class for tracking karma."""
	__tablename__ = "karma"

	string = Column(String, primary_key=True)
	score = Column(Integer, nullable=False)
	nick = Column(String, primary_key=True)

	def __init__(self, string, nick):
		self.string = string
		self.nick = nick
		self.score = 0


def karma(self, event):
	sql_session = get_session()
	before, string, operator = re.search(expression[0], event.arguments).groups()
	string = string.strip().lower()
	nick = getnick(event.source)
	# Find this string or add the row
	item = sql_session.query(Karma).\
	    filter_by(string=string, nick=nick).first()
	if not item:
		item = Karma(string=string, nick=nick)
		sql_session.add(item)
	# Count +/- and alter the score within the range of 5 +/-
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
	sql_session.commit()

expression = ("(^.*[^\w' +-]|^)(.*?)([+]{2,6}|[-]{2,6})", karma)
