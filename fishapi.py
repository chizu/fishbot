#!/usr/bin/python
"""Functions to share with modules isolated from the Fishbot object."""
import importer, time
import sys, os
import urllib, re

#version - set by main class
#execution_time - set by main class
#fishbot - set by main class

def getnick(s):
    """Return an IRC nick from an IRC hostmask"""
    n = s.find("!")
    if n > -1:
        return s[:n]
    else:
        return s

def http_grep(url, regexp):
    page = urllib.urlopen(url).readlines()
    for each in page:
        search = re.search(regexp, each, re.M)
        if search:
            return search.groups()

def say(to, message):
    fishbot.say(to, message)
