#!/usr/bin/python
import pgdb
import sys, os, time, string

db = pgdb.connect(user='fishbot', host='localhost', database='fishbot')
cursor = db.cursor()
# Read only access.
readdb = pgdb.connect(user='fishbotread', host='localhost', database='fishbot')
readcursor = readdb.cursor()

def sql_query(string):
    """Execute a raw query."""
    cursor.execute(string)
    db.commit()
    return cursor.fetchall()

def sql_readonly_query(string):
    """Execute a select query."""
    readcursor.execute(string)
    db.commit()
    return cursor.fetchall()

def add_event(event):
    """Accepts an irclib event, and adds it to the events table."""
    cursor.execute("""INSERT INTO events VALUES (%s, %s, %s, %s, %s);""", (time.strftime("%Y-%m-%dT%H:%M:%S"), event.source(), event.target(), event.eventtype(), string.join(event.arguments())))
    db.commit()

def last(resource, count=1):
    """Return the last 'count' of things said by a nick or channel."""
    cursor.execute("""SELECT * FROM events WHERE source='%s' ORDER BY timestamp DESC LIMIT %s;""" % (resource,count))
    db.commit()
    return cursor.fetchall()

