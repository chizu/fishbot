#!/usr/bin/env python
"""Multiple server IRC protocol support."""
import protocols.sock
import datetime

class IRCEvent(object):
	def __init__(self, server, source, command, params, timestamp=None):
		self.server = server
		self.nick = server.client_nick
		self.source = source
		self.command = command
		self.params = params
		self.target = self.params[0]
		self.arguments = " ".join(self.params)
		if timestamp is None:
			self.timestamp = datetime.datetime.now()
		else:
			self.timestamp = timestamp
		
	def __str__(self):
		return "%s %s || %s %s %s" % (':'.join((self.server.hostname, str(self.server.port))), self.timestamp, self.source, self.command, self.params)

class Client(protocols.sock.Client):
	triggers = protocols.TriggerManager()
	"""IRC server client interface."""
	def __init__(self, nick, realname, hostname, port, ssl=False):
		self.client_nick = nick
		self.realname = realname
		super(Client, self).__init__(hostname, port, ssl)

	def action(self, to, message):
		self.message(to, "\01ACTION " + message + "\01")

	def connect(self):
		super(Client, self).connect()
		self.nick(self.client_nick)
		self.send("USER " + self.client_nick + " 0 * :" + self.realname)
		self.triggers.register("PING", self.pong)
		self.triggers.register("433", self.nickinuse)

	def disconnect(self, reason):
		self.send("QUIT :" + reason)
		super(Client, self).disconnect()

	def do(self, to, string):
		"""Multiline wrapper for actions."""
		for each in string.splitlines():
			self.action(to, each)
		
	def join(self, channel, key=None):
		if key:
			self.send("JOIN " + channel + " " + key)
		else:
			self.send("JOIN " + channel)

	def message(self, to, message):
		self.send("PRIVMSG " + to + " :" + message + "\n")
	
	def nick(self, nick):
		"""Set the nickname."""
		self.send("NICK " + nick)

	def nickinuse(self, event):
		self.client_nick += "_"
		self.nick(self.client_nick)

	def oper(self, username, password):
		self.send("OPER " + username + " " + password)

	def pong(self, event):
		self.send("PONG " + event.arguments)

	def poll(self):
		nextline = ''
		while 1:
			# Handle cut off lines
			buff = nextline + self.recv()
			nextline = ''
			if not buff:
				self.reconnect()
				continue
			lines = buff.split("\n")
			if lines[-1] != '':
				nextline = lines[-1]
				del(lines[-1])
			del(lines[-1])
			# At this point, all lines should be complete, parse stuff up
			for line in lines:
				# Some of RFC 2812 parser
				line = line.strip()
				if line[0] is ':':
					(prefix, command, params) = line[1:].split(" ", 2)
				else:
					(command, params) = line.split(" ", 1)
					prefix = None
				params = params.split(":", 1)
				if len(params) >= 2:
					params = [x.strip() for x in params[0].split()] + [params[1]]
				else:
					params = [x.strip() for x in params[0].split()]
				event = IRCEvent(self, prefix, command, params)
				try:
					self.triggers.trigger(event.command, event)
				except protocols.TriggerMissing:
					print "Unknown protocol reply: ", event
				yield None

	def say(self, to, string):
		"""Multiline wrapper for messages."""
		for each in string.splitlines():
			self.message(to, each)

	def send(self, string):
		"""IRC commands are terminated by a newline."""
		super(Client, self).send(string + "\n")

