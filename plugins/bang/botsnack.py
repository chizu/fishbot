#!/usr/bin/python
"""Cookies are delicious delicacies."""
from fishapi import get_counter
from backend import get_session

sql_session = get_session()
snacks = get_counter("snacks", sql_session)

def bang(pipein, arguments, event):
	snacks.count += 1
	sql_session.commit()
	return (":)", None)
