#!/usr/bin/python
"""Fishbot 2 - More awesome than Fishbot 1.

Fishbot is distributed under the GNU General Public License Version 2.0

Fishbot 2.0 brings dynamic modules, generally cleaner code, more random experiments, and a faster, more stable bot."""
from IRCClient import *
from bang import BangCommand
from string import join
import traceback, re, urllib, sys, xml.dom.minidom, time, os, urlmatch

class Fishbot(LogAllMixin, IRCClient):
    """An IRC bot that listens for commands and performs various functions on the channel."""
    def __init__(self, server = "irc.sandbenders.org", port = 6667, nick = "Fishbot", channels = ["#chshackers","#sandbenders"]):
        self.channels = channels
        IRCClient.__init__(self, server, port)
        self.connect(nick, "Fishbot")	 
	self.last = {}
	self.bang_commands = BangCommand()

    def getText(self, nodelist):
	rc = ""
	for node in nodelist:
	    if node.nodeType == node.TEXT_NODE:
		rc = rc + node.data
	return rc

    def handle_reply(self, prefix, code, params):
	if code == 1:
	    # join channels after welcome message
	    for channel in self.channels:
		self.join(channel)

    def handle_quit(self, nick, reason):
	"""Fishbot has quit, restart it."""
	if nick == self.nick:
	    self.__reinit__()
	    self.connect(self.my_nick, self.realname)

    def respond_to(self, source, to):
	"""Reply to the correct place based on the source and destination"""
	# Target to reply to
	if to in self.channels:
	    # If the request was from a channel, reply to the channel.
	    respond = to
	else:
	    # If the request was from a private message, 
	    # reply to the private message.
	    respond = getnick(source)
	return respond

    def handle_say(self, source, to, message):
	respond = self.respond_to(source, to)

	# Try to leave infinite loops of messages (from other bots typically)
	if (self.last.has_key(getnick(source))):
	    if (self.last[getnick(source)][0] == message and self.last[getnick(source)][1] + 3 > time.time()):
		return
	else:
	    self.last[getnick(source)] = (message, time.time())

	# Match !<stuff> commands.
	match = re.search('^\!(\w+).*$', message)
	if match:
	    command = match.group(1)
	    if not os.path.exists("bang/%s.py" % command):
		if self.bang_commands.has_key(command):
		    self.bang_commands - command
		return
	    try:
		self.bang_commands[command]
		if os.stat("bang/%s.py" % command).st_mtime > os.stat("bang/%s.pyc" % command).st_mtime:
		    self.bang_commands[command] = reload(self.bang_commands[command])
		self.bang_commands[command].handle_say(self, source, to, message)
	    except KeyError:
		self.bang_commands + command
		self.bang_commands[command].handle_say(self, source, to, message)
	    except SystemExit:
		sys.exit()
	    except:
		self.say(respond, "Module %s failed to load: %s" % (command, traceback.format_exc()))

	# This is sadly the original purpose of Fishbot. 
	# !google "not a real cowfish" for what little reasoning there is.
	if re.search("(?=(.*cows.*))(?=(.*go.*))(?=(.*moo.*))", message):
	    self.say(respond, "LIEZ FISH GO MOO!")

	# Keep track of the last message from each user
	self.last[getnick(source)] = (message, time.time())

	# The magic of URL parsing. 
	# I need to kill the number of try, except pairs I used.
        m = urlmatch.regex.search(message)
	if m:
	    try:
		resource = urllib.urlopen(m.group())
	    except:
		return
	    if not (resource.info().getheader('Content-Type').split(';')[0] in ["application/xhtml+xml", "text/html"]):
		if resource.info().getheader('Content-Type').split(';')[0] in ["application/x-bittorrent"]:
		    torrent = resource.readlines()
		    result = re.search("name[0-9]*?:(.*?)12:",torrent[0])
		    if hasattr(result, "group"):
			self.say(respond, "Torrent Name: " + result.group(1))
		else:
		    self.say(respond, "Content Type: " + (resource.info().getheader('Content-Type') or "b0rked webserver"))
		resource.close()
		return
	    try:
		xhtml = resource.readlines()
		dom = xml.dom.minidom.parseString(join(xhtml))
		self.say(respond, "XHTML, Title: " + self.getText(dom.getElementsByTagName("title")[0].childNodes))
	    except:
		for each in xhtml:
		    if re.compile("\<title.*\>(.*)\<\/title\>",re.I).search(each):
			match = re.search("\<title.*\>(.*)\<\/title\>",each,re.I)
			self.say(respond, "Malformed XML, Title: " + match.group(1))
	    resource.close()
	    return

if __name__ == "__main__":
    bot = Fishbot(server = "irc.sandbenders.org", port = 6667, nick = "Fishbot", channels = ["#chshackers","#sandbenders"])
    bot.mainloop()
