#!/usr/bin/python
import fishapi

def events(self, event):
    """Log events into a table with backend.py"""
    fishapi.backend.add_event(event)

expression = ("", events)
