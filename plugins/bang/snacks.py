#!/usr/bin/python
"""Cookies are delicious delicacies."""
from fishapi import get_counter

def bang(pipein, arguments, event):
    snacks = get_counter("snacks")
    return ("%d snacks received." % snacks.count, None)
