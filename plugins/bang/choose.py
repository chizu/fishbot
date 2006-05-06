#!/usr/bin/python
"""!choose - An IRC bot should obviously be making all of the decisions around here.
Usage: <item1> | !choose <item2>,<item3>,<item4>"""
import random,string

def bang(pipein, arguments, events):
    choice = pipein + (pipein and arguments and ',') + arguments
    return ("Entropy decides: " + string.strip(random.choice(choice.split(','))), None)
