#!/usr/bin/python
"""Multiple protocol support interface."""
import threading, traceback

def load():
	import importer
	from glob import glob
	"""On module load, find all the protocols available."""
	submodules = glob("protocols/*")
	submodules.sort()
	__all__ = set()
	for each in submodules:
		each = each.split('/')[-1].split('.')[0]
		__all__.add(each)
	__all__.remove('__init__')
	__all__ = list(__all__)
	__all__.sort()

	for each in __all__:
		module = importer.__import__(name=each, path="protocols")

class TriggerMissing(Exception):
	pass

class TriggerManager(object):
	"""Manage triggers for protocol events."""
	def __init__(self, parent=None):
		self.triggers = {}
		self.parent = parent

	def register(self, command, function, args=()):
		"""Attach a function to a command."""
		if self.triggers.has_key(command):
			self.triggers[command].append((function, args))
		else:
			self.triggers[command] = [(function, args),]

	def trigger(self, command, args):
		"""Execute a command."""
		if self.triggers.has_key(command):
			for each in self.triggers[command]:
				if each[1]:
					each[0](*each[1])
				else:
					each[0](args)
		else:
			if self.parent:
				self.parent.trigger(command, args)
			else:
				raise TriggerMissing("No trigger registered to '%s'." % command)

	def unregister(self, command, function, args=()):
		"""Remove a function from a command."""
		if self.triggers.has_key(command):
			self.triggers[command].remove((function, args))

class ClientThread(threading.Thread):
	def __init__(self, server):
		self.server = server
		super(ClientThread, self).__init__()

	def run(self):
		for each in self.server.poll(): pass
		
class ThreadClient(object):
	"""Threaded server and protocol multiplexing."""
	def __init__(self, servers = {}):
		self.servers = servers
		self.threads = {}

	def start(self):
		"""Start up all registered protocols."""
		for (name, server) in self.servers:
			self.threads[name] = ClientThread(server)
			self.threads[name].start()
		for (name, thread) in self.threads:
			thread.join()

load()
