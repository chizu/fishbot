#!/usr/bin/python
"""!wikipedia - Search wikipedia"""
import re,importer
google = importer.__import__("google", globals(), locals(), "plugins/bang")

def bang(pipein, arguments, event):
	search = pipein or arguments
	return google.bang("site:en.wikipedia.org " + search, "", event)
