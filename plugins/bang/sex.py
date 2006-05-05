#!/usr/bin/python
"""!sex - Spout silly, random porn-like text
Usage: !sex"""
import os

def bang(pipein, arguments, event):
    return (os.popen('sex').readlines(), None)
