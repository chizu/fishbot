#!/usr/bin/python
import sys
import os
import time
import string

from sqlalchemy import create_engine, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

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
    sql_session = get_session()
    sql_session.add(event)
    sql_session.commit()


def last(Event, source=None, target=None, count=1):
    """Return the last 'count' of things said by a nick (source) or 
    channel (target)."""
    sql_session = get_session()
    query = sql_session.query(Event)
    if target:
        filtered = query.filter(Event.target == target)
    elif target and source:
        filtered = query.filter(and_(Event.source == source,
                                     Event.target == target))
    elif source:
        filtered = query.filter(Event.source == source)
    return filtered.order_by(Event.timestamp.desc())[:count]
