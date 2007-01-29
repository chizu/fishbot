#!/usr/bin/env python
"""Fishbot 3 - The movie!

Now in technicolor. Actually now rewritten for modularity and more extensability. This release brings a way for Fishbot to keep data between sessions mostly.

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

class Fishbot(protocols.ThreadClient):
	"""An IRC bot that listens for commands and performs various functions on the channel."""
	def __init__(self, servers):
		#importer.debug = True # Importer debugging
		fishapi.version = "Fishbot 3.0 Beta"
		fishapi.execution_time = time.time()
		fishapi.backend = backend
		fishapi.fishbot = self
		protocols.irc.Client.triggers.register("CTCP", self.message)
		protocols.irc.Client.triggers.register("JOIN", self.message)
		protocols.irc.Client.triggers.register("NICK", self.message)
		protocols.irc.Client.triggers.register("NOTICE", self.message)
		protocols.irc.Client.triggers.register("PART", self.message)
		protocols.irc.Client.triggers.register("PRIVMSG", self.message)
		protocols.irc.Client.triggers.register("QUIT", self.message)
		protocols.irc.Client.triggers.register("INVITE", self.invited)
		super(Fishbot, self).__init__(servers)

	def invited(self, event):
		"""Join a channel/room when invited."""
		event.server.join(event.arguments)

	def on_welcome(self, c, event):
		"""Finished connecting event, join channels."""
		self.join(c, event)

	def message(self, event):
		"""As events occur, call the appropriate hooks in the plugins.

		Any IRC 'event' should call this method, this will log the event and execute the appropriate plugins."""
		# Re-exec fishbot if fishbot itself has changed.
		# This is disabled, it's slightly broken.
		#if os.stat(sys.argv[0]).st_mtime > fishapi.execution_time:
		#	for each in self.servers.values():
		#		each.disconnect("Fishbot has changed enough to require a restart.")
		#	os.execv(sys.argv[0], sys.argv[1:])
		# Execute the plugin tree as required.
		try:
			plugins = importer.__import__("plugins")
			args = event.arguments
			for each in sorted(plugins.expressions):
				match = re.search(each, args)
				if match:
					name = str(plugins.expressions[each])
					print "Event: " + event
					print "Plugin: " + name
					for each in plugins.expressions[each]:
						thread = plugins.PluginThread(each, (self, event))
						thread.start()
		except:
			# A plugin has failed, don't take down the whole bot.
			pass

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
	bot = Fishbot({"chshackers":protocols.irc.Client(nick="Fishbot", realname="Fishbot", hostname="grandpa.chshackers.com", port=6667)})
	bot.servers["chshackers"].join("#chshackers")
	bot.servers["chshackers"].join("#mmo-dev")
	bot.start()
	
if __name__ == "__main__":
    main()
