#!/usr/bin/python
"""Cookies are delicious delicacies."""
import fishapi
snacks = fishapi.Counter(name="snacks")

def bang(pipein, arguments, event):
	return ("%d snacks received." % snacks.count, None)
