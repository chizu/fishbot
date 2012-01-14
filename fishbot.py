#!/usr/bin/env python
"""Fishbot 3 - The movie!

Now in technicolor. Actually now rewritten for modularity and more extensability.

Fishbot is distributed under the GNU General Public License Version 2.0.
"""
# Fishbot specific
import protocols
import plugins
import backend
import fishapi
import importer

# Python builtins
import threading, time, os, sys, traceback, re

class Fishbot(protocols.ThreadManager):
	"""An IRC bot that listens for commands and performs various functions on the channel."""
	def __init__(self, servers):
		#importer.debug = True # Importer debugging
		fishapi.version = "Fishbot 3.1 Beta"
		fishapi.execution_time = time.time()
		fishapi.backend = backend
		fishapi.fishbot = self
		protocols.generic.Client.triggers.register("message", self.messaged)
		protocols.generic.Client.triggers.register("invite", self.invited)
		super(Fishbot, self).__init__(servers)

	def invited(self, event):
		"""Join a channel/room when invited."""
		event.server.join(event.arguments)
		event.server.channels.append(event.arguments)

	def messaged(self, event):
		"""As messages occur, call the appropriate hooks in the plugins.

		Any server message should call this method, this will execute the appropriate plugins."""
		# Re-exec fishbot if fishbot itself has changed.
		# This is disabled, it's slightly broken.
		#if os.stat(sys.argv[0]).st_mtime > fishapi.execution_time:
		#	for each in self.servers.values():
		#		each.disconnect("Fishbot has changed enough to require a restart.")
		#	os.execv(sys.argv[0], sys.argv[1:])
		# Execute the plugin tree as required.
		plugins = importer.__import__("plugins")
		print "Event: " + str(event)
		for each in sorted(plugins.expressions):
			match = re.search(each, event.arguments)
			if match:
				name = str(plugins.expressions[each])
				print "Expression: " + str(each)
				for each in plugins.expressions[each]:
					print "Plugin: " + str(each)
					thread = plugins.PluginThread(each, (self, event))
					thread.start()

	def respond_to(self, source, to):
		"""Reply to the correct place based on the source and destination"""
		# Target to reply to
		if to[0] is "#":
			# If the request was from a channel, reply to the channel.
			respond = to
		else:
			# If the request was from a private message, 
			# reply to the private message.
			respond = source.split("!")[0]
		return respond

def main():
	import protocols.irc
	bot = Fishbot({"chshackers":protocols.irc.Client(nick="Fishbot", realname="Fishbot", hostname="grandpa.chshackers.com", port=6667)})
	bot.servers["chshackers"].join("#chshackers")
	bot.servers["chshackers"].join("#mmo-dev")
	bot.start()
	
if __name__ == "__main__":
    main()
