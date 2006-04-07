#!/usr/bin/python
def events(self, event):
    """Log events into a table with backend.py"""
    self.backend.add_event(event)

expression = ("", events)
