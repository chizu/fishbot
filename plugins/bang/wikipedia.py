#!/usr/bin/python
"""!wikipedia - Search wikipedia"""
import re,importer
__import__ = importer.__import__
import plugins.bang.google

def bang(pipein, arguments, event):
	search = pipein or arguments
	return google.bang("site:en.wikipedia.org " + search, "", event)
