#!/usr/bin/python
"""Cookies are delicious delicacies."""
import fishapi
snacks = fishapi.Counter(name="snacks")

def bang(pipein, arguments, event):
	snacks.count += 1
	return (":)", None)
