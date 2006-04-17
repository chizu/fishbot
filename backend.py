#!/usr/bin/python
import pgdb
import sys, os, time, string

db = pgdb.connect(user='fishbot', host='localhost', database='fishbot')
# Read only access.
readdb = pgdb.connect(user='fishbotread', host='localhost', database='fishbot')

def sql_query(string, readonly=True):
    """Execute a raw query.

    Accepts the SQL query string, and a parameter to govern 'writes' to the database (i.e. SELECT is only allowed while readonly is True)."""
    if readonly:
        cursor = readdb.cursor()
    else:
        cursor = db.cursor()
    cursor.execute(string)
    db.commit()
    return cursor.fetchall()

def add_event(event):
    """Accepts an irclib event, and adds it to the events table."""
    cursor = db.cursor()
    cursor.execute("""INSERT INTO events VALUES (%s, %s, %s, %s, %s);""", (time.strftime("%Y-%m-%dT%H:%M:%S"), event.source(), event.target(), event.eventtype(), string.join(event.arguments())))
    print dir(db)
    db.commit()

def last(resource, count=1):
    """Return the last 'count' of things said by a nick or channel."""
    cursor = readdb.cursor()
    cursor.execute("""SELECT * FROM events WHERE source='%s' ORDER BY timestamp DESC LIMIT %s;""" % (resource,count))
    db.commit()
    return cursor.fetchall()
