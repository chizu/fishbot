#!/usr/bin/python
"""Cookies are delicious delicacies."""
import fishapi
def bang(pipein, arguments, event):
    return ("%d snacks received." % fishapi.backend.sql_query("SELECT count(*) FROM events WHERE arguments~'!botsnack';")[0][0], None)
