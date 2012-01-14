#!/usr/bin/python
"""Please, stop with the beatings."""
from fishapi import get_counter

def bang(pipein, arguments, event):
    smacks = get_counter("smacks")
    return ("%d smacks received." % smacks.count, None)
