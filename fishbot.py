#!/usr/bin/python
"""Fishbot 3 - The movie!

Now in technicolor. Actually now rewritten for modularity and more extensability. This release brings a way for Fishbot to keep data between sessions mostly.

Fishbot is distributed under the GNU General Public License Version 2.0
"""
# IRC libraries
import irclib
import ircbot

# Fishbot specific
import plugins
import backend
import importer

# Python builtins
import thread, time, os, sys, traceback
#import traceback, re, urllib, sys, xml.dom.minidom, time, os, urlmatch

class Fishbot(ircbot.SingleServerIRCBot):
    """An IRC bot that listens for commands and performs various functions on the channel."""
    def __init__(self, server = "irc.sandbenders.org", port = 6667, nick = "Fishbot", channels = ["#chshackers"]):
	irclib.DEBUG = 1 # Debugging output on the console
        self.join = channels
        self.version = "Fishbot 3.0 Alpha"
        self.execution_time = time.time()
        self.backend = backend
	ircbot.SingleServerIRCBot.__init__(self, [(server, port)], nick, nick)

    def on_nicknameinuse(self, c, event):
	self.connection.nick(self.connection.get_nickname() + "_")

    def on_welcome(self, c, event):
	for channel in self.join:
	    self.connection.join(channel)

    def on_kick(self, c, event):
        self.on_welcome(c, event)
    
    def on_ctcp(self, c, event):
        self.on_msg(c, event)
        
    def on_privmsg(self, c, event):
        self.on_msg(c, event)

    def on_pubmsg(self, c, event):
        self.on_msg(c, event)
	to = event.target()
	source = event.source()

	# Try to leave infinite loops of messages (from other bots typically)
        """
	if (self.last(source)):
	    if (self.last(source).message == event.arguments()[0] and self.last[source].message_time + 3 > time.time()):
		return
	else:
	    self.last(source).message_time = time.time()
	    self.last(source).message = event.arguments()[0]
        """
	#thread.start_new_thread(self.msg,(to, event.arguments()[0]))

    def on_msg(self, c, event):
        # Re-exec fishbot if fishbot itself has changed.
        if os.stat(sys.argv[0]).st_mtime > self.execution_time:
            self.disconnect("Fishbot has changed enough to require a restart.")
            os.execv(sys.argv[0], sys.argv[1:])
        # Execute the plugin tree as required.
        plugins = importer.__import__("plugins")
        for each in plugins.expressions:
            match = each.search(event.arguments()[0])
            if match:
                print plugins.expressions[each]
                thread.start_new_thread(plugins.expressions[each],(self,event))

    def say(self, to, message):
	"""Multiple line wrapper for irclib.connection.privmsg"""
	for each in message.split("\n"):
	    if each:
		self.connection.privmsg(to, each)

    def action(self, to, message):
	"""CTCP ACTION wrapper for irclib.connection.ctcp"""
	for each in message.split("\n"):
	    if each:
		self.connection.ctcp("ACTION", to, each)
                
    def respond_to(self, source, to):
	"""Reply to the correct place based on the source and destination"""
	# Target to reply to
	if to in self.channels:
	    # If the request was from a channel, reply to the channel.
	    respond = to
	else:
	    # If the request was from a private message, 
	    # reply to the private message.
	    respond = irclib.nm_to_n(source)
	return respond

    def getnick(self, s):
        """Return an IRC nick from an IRC hostmask"""
        n = s.find("!")
        if n > -1:
            return s[:n]
        else:
            return s
    
def main():
    bot = Fishbot(channels = ["#botfucking"])
    bot.start()

if __name__ == "__main__":
    main()
