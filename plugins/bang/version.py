#!/usr/bin/python
"""!version - Fishbot's version and other info."""
import fishapi

def bang(pipein, arguments, event):
    return (fishapi.version + " - SVN at http://fishbot.spicious.com/svn/fishbot", None)
