#!/usr/bin/python
"""!update - Update Fishbot to the latest git.
Usage: !update"""
import os

def bang(pipein, arguments, event):
    for each in os.popen('git pull').readlines():
        print each
    return (None, 'performs major surgery on itself.')
