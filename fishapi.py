#!/usr/bin/python
"""Functions to share with modules isolated from the Fishbot object."""
import sys
import os
import time
import string
import urllib
import re

from sqlalchemy import Column, Integer, String

import importer
from backend import DatabaseObject, get_session

#version - string set by main class
#execution_time - time set by main class

# Set a user agent in case later code attempts to use urllib
urllib.URLopener.version = """Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1b2) Gecko/20060906 Firefox/2.0b2"""

def getnick(s):
	"""Return an IRC nick from an IRC hostmask"""
	n = s.find("!")
	if n > -1:
		return s[:n]
	else:
		return s

def http_grep(url, regexp):
	"""Search the page returned by 'url' line by line for 'regexp'.

	Returns the first matching groups."""
	page = urllib.urlopen(url).readlines()
	for each in page:
		search = re.search(regexp, each, re.M)
		if search:
			return search.groups()

class Counter(DatabaseObject):
	"Count things!"
	__tablename__ = 'counters'
	name = Column(String, primary_key=True)  # name of the counter
	count = Column(Integer)  # the count

	def __init__(self, name):
		self.name = name
		self.count = 0

def get_counter(name, sql_session=None):
	if not sql_session:
		sql_session = get_session()
	counter = sql_session.query(Counter).filter_by(name=name).first()
	if not counter:
		counter = Counter(name=name)
		sql_session.add(counter)
		sql_session.commit()
	return counter
