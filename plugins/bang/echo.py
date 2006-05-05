#!/usr/bin/python
"""!echo - Echo things
Usage: !echo <text>"""
import re,os

def bang(pipein, arguments, event):
    return ((pipein + arguments) or "Mooo", None)
