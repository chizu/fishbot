#!/usr/bin/env python
"""Fishbot 3 - The movie!

Now in technicolor. Actually now rewritten for modularity and more extensability. This release brings a way for Fishbot to keep data between sessions mostly.

Fishbot is distributed under the GNU General Public License Version 2.0.
"""
# IRC libraries
import irclib
import ircbot

# Fishbot specific
import plugins
import backend
import fishapi
import importer

# Python builtins
import thread, time, os, sys, traceback, string, re

# Set a user agent in case later code attempts to use urllib
import urllib
urllib.URLopener.version = """Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1b2) Gecko/20060906 Firefox/2.0b2"""

class Fishbot(ircbot.SingleServerIRCBot):
    """An IRC bot that listens for commands and performs various functions on the channel."""
    def __init__(self, server = "irc.chshackers.com", port = 6667, nick = "Fishbot", channels = []):
	#irclib.DEBUG = True # Message debugging
        #importer.debug = True # Importer debugging
        self.join_channels = channels
        fishapi.version = "Fishbot 3.0 Beta"
        fishapi.execution_time = time.time()
        fishapi.backend = backend
        fishapi.fishbot = self
	ircbot.SingleServerIRCBot.__init__(self, [(server, port)], nick, nick)

    def quit(self, c, event):
        if not self.connection.connected:
            self.connection.connect()
        self.join(c, event)

    def join(self, c, event):
        """Join the configured channels.

        Fishbot.join_channels specifies the channels this joins."""
        if hasattr(self, "oper"):
            self.connection.oper(self.oper["username"], self.oper["password"])
	for channel in self.join_channels:
	    self.connection.join(channel)
            if hasattr(self, "sayonjoin"):
                self.say(channel, self.sayonjoin)

    def on_nicknameinuse(self, c, event):
        """Nickname in use event, create a new nickname."""
	self.connection.nick(self.connection.get_nickname() + "_")

    def on_welcome(self, c, event):
        """Finished connecting event, join channels."""
        self.join(c, event)

    def on_ctcp(self, c, event):
        """CTCP events, typically CTCP ACTION"""
        self.on_msg(c, event)

    def on_join(self, c, event):
        """User joined a channel event."""
        self.on_msg(c, event)

    def on_part(self, c, event):
        """User left a channel event."""
        self.on_msg(c, event)

    def on_quit(self, c, event):
        """User quit IRC event."""
        self.on_msg(c, event)

    def on_privmsg(self, c, event):
        """Private message event."""
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
        """As events occur, call the appropriate hooks in the plugins.

        Any IRC 'event' should call this method, this will log the event and execute the appropriate plugins."""
        #print fishapi.backend.last(event.source())[0][0]
        # Re-exec fishbot if fishbot itself has changed.
        if os.stat(sys.argv[0]).st_mtime > fishapi.execution_time:
            self.disconnect("Fishbot has changed enough to require a restart.")
            os.execv(sys.argv[0], sys.argv[1:])
        # Execute the plugin tree as required.
        try:
            plugins = importer.__import__("plugins")
            args = string.join(event.arguments())
            
            for each in sorted(plugins.expressions):
                match = re.search(each, args)
                if match:
                    print "Event called: " + str(plugins.expressions[each])
                    for each in plugins.expressions[each]:
                        thread.start_new_thread(each,(self,event))
        except:
            # A plugin has failed, report why, but don't take down the whole bot.
            traceback.print_last()

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
    bot = Fishbot(channels = ["#chshackers", "#mmo-dev"])
    bot.start()

if __name__ == "__main__":
    main()
