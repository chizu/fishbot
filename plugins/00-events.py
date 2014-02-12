#!/usr/bin/python
import backend

def events(self, event):
    """Log events into a table with backend.py"""
    backend.add_event(event)

expression = ("", events)
