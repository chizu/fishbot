#!/usr/bin/python
import pgdb
import sys, os, time

db = pgdb.connect(user='fishbot', host='localhost', database='fishbot')
cursor = db.cursor()

def sql_query(string):
    """Execute a raw query."""
    cursor.execute(string)
    return cursor.fetchall()

def add_event(event):
    """Accepts an irclib event, and adds it to the events table."""
    arguments = str(event.arguments()).replace('[','{').replace(']','}').replace('\'','"')
    cursor.execute("""INSERT INTO events VALUES ('%s', '%s', '%s', '%s');""" % (time.strftime("%Y-%m-%dT%H:%M:%S"), event.source(), event.target(), arguments))
    db.commit()

def last(resource, count=1):
    """Return the last 'count' of things said by a nick or channel."""
    cursor.execute("""SELECT * FROM events WHERE source='%s' ORDER BY timestamp DESC LIMIT %s;""" % (resource,count))
    return cursor.fetchall()
