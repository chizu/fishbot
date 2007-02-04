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

# Set a user agent in case later code attempts to use urllib
import urllib
urllib.URLopener.version = """Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1b2) Gecko/20060906 Firefox/2.0b2"""

class Fishbot(protocols.ThreadManager):
	"""An IRC bot that listens for commands and performs various functions on the channel."""
	def __init__(self, servers):
		#importer.debug = True # Importer debugging
		fishapi.version = "Fishbot 3.1 Alpha"
		fishapi.execution_time = time.time()
		fishapi.backend = backend
		fishapi.fishbot = self
		protocols.irc.Client.triggers.register("CTCP", self.messaged)
		protocols.irc.Client.triggers.register("JOIN", self.messaged)
		protocols.irc.Client.triggers.register("NICK", self.messaged)
		protocols.irc.Client.triggers.register("NOTICE", self.messaged)
		protocols.irc.Client.triggers.register("PART", self.messaged)
		protocols.irc.Client.triggers.register("PRIVMSG", self.messaged)
		protocols.irc.Client.triggers.register("QUIT", self.messaged)
		protocols.irc.Client.triggers.register("INVITE", self.invited)
		super(Fishbot, self).__init__(servers)

	def invited(self, event):
		"""Join a channel/room when invited."""
		event.server.join(event.arguments)

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
