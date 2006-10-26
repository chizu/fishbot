#!/usr/bin/python
"""Cookies are delicious delicacies."""
import fishapi
def bang(pipein, arguments, event):
    return ("%d snacks received." % fishapi.backend.sql_query("select count(*) as count, split_part( source, '!', 1) as nick FROM events WHERE arguments ~'!botsnack' GROUP BY nick;")[0][0], None)
