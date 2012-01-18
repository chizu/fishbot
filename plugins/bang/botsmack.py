#!/usr/bin/python
"""Please, stop with the beatings."""
from fishapi import get_counter
from backend import get_session

sql_session = get_session()
smacks = get_counter("smacks", sql_session)

def bang(pipein, arguments, event):
    smacks.count += 1
    sql_session.commit()
    return (":(", None)
