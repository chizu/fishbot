#!/usr/bin/python
import importer, time
import sys, os

version = "Fishbot 3.0 - Beta"
#execution_time - set by main class
#fishbot - set by main class

def getnick(s):
    """Return an IRC nick from an IRC hostmask"""
    n = s.find("!")
    if n > -1:
        return s[:n]
    else:
        return s

def halt(message):
    fishbot.disconnect(message)
    sys.exit(0)

def restart(message):
    fishbot.disconnect(message)
    os.execv(sys.argv[0], sys.argv[1:])
    sys.exit(0)

def http_grep(url, regexp):
    page = urllib.urlopen(url).readlines()
    for each in page:
        search = re.search(regexp, each, re.M)
        if search:
            return search.groups()
