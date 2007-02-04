#!/usr/bin/python
"""!wikipedia - Search wikipedia"""
import urllib,re
import plugins.bang.google

def bang(pipein, arguments, event):
	search = pipein or arguments
	return plugins.bang.google.bang("site:en.wikipedia.org " + search, "", event)
