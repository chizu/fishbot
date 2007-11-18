#!/usr/bin/env python
"""Multiple server IRC protocol support."""
import protocols.sock

def Property(function):
	import sys
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

class IRCEvent(protocols.sock.SocketEvent):
	pass
		
class Client(protocols.sock.Client):
	"""IRC server client interface."""
	triggers = protocols.TriggerManager(protocols.sock.Client.triggers)
	protocol = "IRC"
	def __init__(self, nick, realname, hostname, port, ssl=False):
		self._nick = nick
		self.realname = realname
		self.channels = []
		self.triggers.register("PING", self.pong)
		self.triggers.register("433", self.nickinuse)
		self.triggers.alias("CTCP", "message")
		self.triggers.alias("JOIN", "message")
		self.triggers.alias("NICK", "message")
		self.triggers.alias("NOTICE", "message")
		self.triggers.alias("PART", "message")
		self.triggers.alias("PRIVMSG", "message")
		self.triggers.alias("QUIT", "message")
		self.triggers.alias("INVITE", "invite")
		super(Client, self).__init__(hostname, port, ssl)

	def action(self, to, message):
		self.message(to, "\01ACTION " + message + "\01")

	def connect(self):
		"""Connect to IRC, mention nick name """
		super(Client, self).connect() # Do the socket connection
		self.nick = self._nick
		self.send("USER " + self.nick + " 0 * :" + self.realname)
		for each in self.channels:
			self.join(each, rejoin=True)

	def disconnect(self, reason=""):
		self.send("QUIT :" + reason)
		super(Client, self).disconnect()

	def do(self, to, string):
		"""Multiline wrapper for actions."""
		for each in string.splitlines():
			self.action(to, each)
		
	def join(self, channel, key=None, rejoin=False):
		if key:
			self.send("JOIN " + channel + " " + key)
		else:
			self.send("JOIN " + channel)
		if not rejoin:
			self.channels.append(channel)

	def message(self, to, message):
		self.send("PRIVMSG " + to + " :" + message + "\n")

	@Property
	def nick():
		"""Set the nickname."""
		def fget(self):
			return self._nick
		def fset(self, nick):
			self.send("NICK " + nick)
			self._nick = nick

	def nickinuse(self, event):
		self._nick += "_"
		self.nick = self._nick

	def oper(self, username, password):
		self.send("OPER " + username + " " + password)

	def pong(self, event):
		self.send("PONG " + event.target)

	def poll(self):
		nextline = ''
		while 1:
			# Handle cut off lines
			buff = nextline + self.recv()
			nextline = ''
			if not buff:
				Client.reconnect(self)
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
				event = IRCEvent(self, prefix, params[0], command, params[1:])
				try:
					self.triggers.trigger(event.command, event)
				except protocols.TriggerMissing:
					print "Unhandled: ", event
				yield None

	def say(self, to, string):
		"""Multiline wrapper for messages."""
		for each in string.splitlines():
			self.message(to, each)

	def send(self, string):
		"""IRC commands are terminated by a newline."""
		print "Sending:", string
		super(Client, self).send(string + "\n")
