#!/usr/bin/python
"""!update - Update Fishbot to the latest SVN.
Usage: !update"""
import os

def bang(pipein, arguments, event):
    for each in os.popen('svn up').readlines():
        print each
    return (None, 'performs major surgery on itself.')
