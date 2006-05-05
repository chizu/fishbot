#!/usr/bin/python
"""!morse - Morse encoding
Usage: <text> | !morse"""
import re,os

def bang(pipein, arguments, event):
    return (os.popen('echo "%s" | cwtext' % re.escape(pipein)).readlines(), None)
