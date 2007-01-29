#!/usr/bin/python
"""Please, stop with the beatings."""
import fishapi
def bang(pipein, arguments, event):
    return ("%d smacks received." % fishapi.backend.sql_query("SELECT count(*) FROM events WHERE arguments~'!botsmack';")[0][0], None)
