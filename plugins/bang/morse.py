#!/usr/bin/python
"""!morse - Morse encoding
Usage: <text> | !morse"""
import re
import os

def bang(pipein, arguments, event):
     lines = os.popen('echo "%s" | morse -s' % re.escape(pipein)).readlines()
     return ("".join(lines.split('/n')), None)
