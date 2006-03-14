#!/usr/bin/python
"""Fishbot 3 - The movie!

Now in technicolor. Actually now rewritten for modularity and more extensability. This release brings a way for Fishbot to keep data between sessions mostly.

Fishbot is distributed under the GNU General Public License Version 2.0
"""
# IRC libraries
import irclib
import ircbot

# Fishbot specific
import matches
import backend
import importer

# Python builtins
import thread, time, re, os, traceback
#import traceback, re, urllib, sys, xml.dom.minidom, time, os, urlmatch

class Fishbot(ircbot.SingleServerIRCBot):
    """An IRC bot that listens for commands and performs various functions on the channel."""
    def __init__(self, server = "irc.sandbenders.org", port = 6667, nick = "Fishbot", channels = ["#chshackers"]):
	irclib.DEBUG = 1
        self.join = channels
	ircbot.SingleServerIRCBot.__init__(self, [(server, port)], nick, nick)
	#self.bang_commands = bang.BangCommand()
        self.plugins = {'bang':__import__('bang')}
        self.bang_commands.keys = self.plugins['bang'].keys

    def on_nicknameinuse(self, c, event):
	self.connection.nick(self.connection.get_nickname() + "_")

    def on_welcome(self, c, event):
	for channel in self.join:
	    self.connection.join(channel)

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
	self.bang(event)

    def say(self, to, message):
	"""Multiple line wrapper for irclib.connection.privmsg"""
	for each in message.split("\n"):
	    if each:
		self.connection.privmsg(to, each)

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

    def bang(self, event):
        match = re.search('^\!(\w+).*$', event.arguments()[0])
        if match:
            module = importer.__import__(match.group(1), globals(), locals(), 'bang')
            print module
            if module:
                module.handle_say(self, event.source(), event.target(), event.arguments()[0])

    def bang_execute(self, event):
	"""Load an execute modules from the bang package directory."""
	match = re.search('^\!(\w+).*$', event.arguments()[0])
	if match:
	    command = match.group(1)
	    # Make sure the file exists, if not delete the module.
	    # If it does, load or update the module
	    if not os.path.exists(self.bang_commands.path + "/%s.py" % command):
		if self.bang_commands.has_key(command):
		    self.bang_commands - command
		return
	    try:
		self.bang_commands[command]
		if os.stat("bang/%s.py" % command).st_mtime > os.stat("bang/%s.pyc" % command).st_mtime:
		    self.bang_commands[command] = reload(self.bang_commands[command])
		self.bang_commands[command].handle_say(self, event.source(), event.target(), event.arguments()[0])
	    except KeyError:
		self.bang_commands + command
		self.bang_commands[command].handle_say(self, event.source(), event.target(), event.arguments()[0])
	    except SystemExit:
		sys.exit()
	    except:
		self.say(irclib.nm_to_n(event.source()), "Module %s failed to load: %s" % (command, traceback.format_exc()))

    
def main():
    bot = Fishbot(channels = ["#botfucking"])
    bot.start()

if __name__ == "__main__":
    main()
