#!/usr/bin/python
import sys
import os
import time
import string

from sqlalchemy import create_engine, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

# locking
import thread
backend_lock = thread.allocate_lock()

engine = create_engine('postgresql:///fishbot')
# SQLAlchemy base
DatabaseObject = declarative_base()
Session = sessionmaker(bind=engine)


def get_session():
    # Naively return a database session
    DatabaseObject.metadata.create_all(engine)
    return Session()


def add_event(event):
    """Accepts an IRCEvent, and adds it to the events table."""
    backend_lock.acquire()
    sql_session = get_session()
    sql_session.add(event)
    sql_session.commit()
    backend_lock.release()


def last(Event, resource, count=1):
    """Return the last 'count' of things said by a nick or channel."""
    sql_session = get_session()
    return sql_session.query(Event).\
        filter(or_(Event.source == resource, Event.target == resource)).\
        order_by(Event.timestamp.desc())[:count]
