#!/usr/bin/env python
import socket, protocols

class Client(object):
	triggers = protocols.TriggerManager()
	def __init__(self, hostname, port, ssl=False):
		self.hostname = hostname
		self.port = port
		self.ssl = ssl
		self.triggers = protocols.TriggerManager(self.triggers)
		self.connect()

	def connect(self):
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
		if self.ssl:
			del(self.ssl)
		self.sock.close()
		del(self.sock)

	def poll(self):
		pass
	
	def reconnect(self):
		self.disconnect()
		self.connect()

	def recv(self):
		if self.ssl:
			return self.ssl.read()
		else:
			return self.sock.recv(1024)

	def send(self, string):
		if self.ssl:
			length = self.ssl.write(string)
		else:
			length = self.sock.send(string)
		if length == len(string):
			return 
		else:
			print length
			raise socket.error("Sending data failed.")