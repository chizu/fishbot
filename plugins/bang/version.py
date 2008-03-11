#!/usr/bin/python
"""!version - Fishbot's version and other info."""
import fishapi

def bang(pipein, arguments, event):
    return (fishapi.version + " -  git repo at git://spicious.com/home/chizu/git/fishbot", None)
