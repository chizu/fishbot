#!/usr/bin/python
"""!fortune - Print out a fortune.
Usage: !fortune <fortune file>"""
import os,re

def bang(pipein, arguments, event):
    if len(arguments) > 0:
        fortune_dictionary = arguments
    else:
        fortune_dictionary = ""
    return (os.popen('fortune -n 500 -s %s' % re.escape(fortune_dictionary)).readlines(), None)
