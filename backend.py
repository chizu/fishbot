#!/usr/bin/python
import pgdb
import sys, os, time, string
import chesterfield

# locking
import thread
backend_lock = thread.allocate_lock()

# Standard SQL access.
writedb = pgdb.connect(user='fishbot', database='fishbot')
# Read only access.
readdb = pgdb.connect(user='fishbotread', database='fishbot')

# Chesterfield derived objects
DatabaseObject = chesterfield.Chesterfield(user='fishbot', database='fishbot').object
#ReadOnlyDatabaseObject = chesterfield.DatabaseObject(user='fishbotread', host='localhost', database='fishbot')

def sql_query(string, readonly=True):
    """Execute a raw query.

    Accepts the SQL query string, and a parameter to govern 'writes' to the database (i.e. SELECT is only allowed while readonly is True)."""
    if readonly:
        db = readdb
    else:
        db = writedb
    backend_lock.acquire()
    cursor = db.cursor()
    try:
        cursor.execute(string)
        db.commit()
        backend_lock.release()
        return cursor.fetchall()
    except:
        db.rollback()
        backend_lock.release()
        raise
    
def add_event(event):
    """Accepts an IRCEvent, and adds it to the events table."""
    backend_lock.acquire()
    cursor = writedb.cursor()
    cursor.execute("""INSERT INTO events VALUES (%s, %s, %s, %s, %s);""", (time.strftime("%Y-%m-%dT%H:%M:%S"), event.source, event.target, event.command, event.arguments))
    writedb.commit()
    backend_lock.release()

def last(resource, count=1):
    """Return the last 'count' of things said by a nick or channel."""
    return sql_query("""SELECT * FROM events WHERE source='%s' OR target='%s' ORDER BY timestamp DESC LIMIT %s;""" % (resource, resource, count))
