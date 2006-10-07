#!/usr/bin/python
"""!ddate - Print out the discordian date..
Usage: !ddate [+format]"""
import os,re

def bang(pipein, arguments, event):
    if len(arguments) > 0:
        options = arguments
    else:
        options = ""
    return (os.popen('ddate %s' % re.escape(options)).readlines(), None)
