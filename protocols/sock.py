#!/usr/bin/env python
import socket
import protocols.generic

class SocketEvent(protocols.generic.Event):
	pass

class Client(protocols.generic.Client):
	"""Simple socket protocol, base class for socket based protocols."""
	triggers = protocols.TriggerManager(protocols.generic.Client.triggers)
	def __init__(self, hostname, port, ssl=False):
		self.hostname = hostname
		self.port = port
		self.ssl = ssl
		self.triggers = protocols.TriggerManager(self.triggers)
		self.connect()

	def connect(self):
		"""Called to initialize the connection, might be called later to reconnect in case of failure."""
		# We're using getaddrinfo for IPv6 support
		sockinfo = socket.getaddrinfo(self.hostname, self.port)
		for each in sockinfo:
			if each[1] == socket.SOCK_STREAM:
				self.sock = socket.socket(*each[:3])
				self.sock.connect(each[4])
				break
		if not hasattr(self, "sock"):
			raise socket.error("No suitable addresses found for %s:%s." % (hostname,port))
		if self.ssl:
			self.ssl = socket.ssl(self.sock)
		else:
			self.ssl = False

	def disconnect(self):
		"""Called to disconnect, may be called multiple times in case of reconnecting."""
		if self.ssl:
			self.ssl.close()
			del(self.ssl)
		self.sock.close()
		del(self.sock)

	def poll(self):
		"""Generator for polling server events. This will be called as often as it yields, and will exit upon returning."""
		return
	
	def reconnect(self):
		"""Called to reconnect in case of failure or reloading."""
		self.disconnect()
		self.connect()

	def recv(self):
		"""Called to retrieve raw data from the socket."""
		if self.ssl:
			return self.ssl.read()
		else:
			return self.sock.recv(1024)

	def send(self, string):
		"""Called to send raw data out the socket."""
		try:
			if self.ssl:
				length = self.ssl.write(string)
			else:
				length = self.sock.send(string)
		except socket.error, v:
			if v[0] == 32: # Broken pipe
				self.disconnect()
				self.connect()
			else: # Unknown socket error
				self.disconnect()
				raise
		if length == len(string):
			return 
		else:
			raise socket.error("Sending data failed.")
