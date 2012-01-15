#!/usr/bin/env python
"""This is an example protocol interface.

To implement protocols, you should subclass this and implement as many methods as are relevant to the protocol you are writing support for."""
import sys
import datetime

from sqlalchemy import Column, Integer, String, DateTime

import protocols
from backend import DatabaseObject

def Property(function):
	keys = 'fget', 'fset', 'fdel'
	func_locals = {'doc':function.__doc__}
	def probeFunc(frame, event, arg):
		if event == 'return':
			locals = frame.f_locals
			func_locals.update(dict((k,locals.get(k)) for k in keys))
			sys.settrace(None)
		return probeFunc
	sys.settrace(probeFunc)
	function()
	return property(**func_locals)

class Event(DatabaseObject):
	"""Server triggered event."""
	__tablename__ = 'events'

	id = Column(Integer, primary_key=True)
	timestamp = Column(DateTime(timezone=True))
	source = Column(String)
	target = Column(String)
	command = Column(String)
	arguments = Column(String)

	def __init__(self, server, source, target, command, params, timestamp=None):
		self.server = server
		self.source = source
		self.target = target
		self.command = command
		self.params = params
		self.arguments = " ".join(params)
		if timestamp is None:
			self.timestamp = datetime.datetime.now()
		else:
			self.timestamp = timestamp

	def __str__(self):
		"""URL style representation of an event."""
		return "%s://%s->%s@%s:%s/%s/%s" % (self.server.protocol, self.source, self.target, self.server.hostname, str(self.server.port), self.command, self.arguments)

class Client(object):
	"""Generic client-server interface.

	When creating a new protocol interface, you should inherit from this and overload any functionality required."""
	triggers = protocols.TriggerManager()
	protocol = "generic"
	
	def __init__(self, nick, hostname, port, realname=None, password=None, ssl=False):
		self.nick = nick

	def action(self, to, message):
		"""Used to implement emotes.

		to is the target, message is the emote string."""
		pass

	def connect(self):
		"""Setup the server connection.

		May be called multiple times from a disconnected context."""
		pass

	def disconnect(self):
		"""Tear down the server connection.

		May be called multiple times from a connected context."""
		pass

	def do(self, to, actions):
		"""Multiple actions passed in one string.

		to is the target.
		actions will be a string with one action per line."""
		for each in actions.splitlines():
			self.action(to, each)

	def join(self, channel, key=None):
		"""Join a group, room, channel, conversation, etc...

		channel is some name for the group you're joining.
		key is optionally a password or key phrase."""
		pass

	def message(self, to, message):
		"""Send a message to some group or person.

		to is the target.
		message is a string containing the message to send."""
		pass

	@Property
	def nick():
		"""Set the bot's name.

		nick is the identifier string for the bot to use."""
		def fget(self):
			return self._nick
		def fset(self, nick):
			self._nick = nick

	def oper(self, username, password):
		"""Identify on a server level.

		Should the bot need to login as a oper or wizard or equivalent on this protocol, implement this."""
		pass

	def poll(self):
		"""Poll for new server events.

		This should return a Python generator that returns server events in order.

		To be efficient, this should block while nothing is happening."""
		pass

	def recv(self, string):
		"""Do the low level receiving."""
		pass

	def say(self, to, string):
		"""Send multiple messages.

		to is the target to send to.
		string is a line delimited set of messages to send."""
		for each in string.splitlines():
			self.message(to, each)

	def send(self, string):
		"""Do the low level sending.

		This can do any low level alteration of string before."""
		pass
