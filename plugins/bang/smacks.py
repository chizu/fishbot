#!/usr/bin/python
"""Please, stop with the beatings."""
import fishapi
smacks = fishapi.Counter(name="smacks")

def bang(pipein, arguments, event):
    return ("%d smacks received." % smacks.count, None)
