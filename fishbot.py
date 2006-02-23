#!/usr/bin/python
"""Fishbot - The least thought out IRC bot ever.

Fishbot is distributed under the GNU General Public License Version 2.0"""
import re, os, urllib, sys, xml.dom.minidom, string, time
import urlmatch
from IRCClient import *

def getText(nodelist):
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc

class Y66(LogAllMixin, IRCClient):
    def __init__(self, server = "irc.sandbenders.org", port = 6667, nick = "Fishbot", channels = ["#chshackers","#sandbenders","#botfucking"]):
        self.channels = channels
        IRCClient.__init__(self, server, port)
        self.connect(nick, "Fishbot")
        self.re = urlmatch.regex
	self.moo = re.compile("cows.*go.*moo|moo.*go.*cows|go.*cows.*moo|go.*moo.*cows|oom.*og.*swoc", re.I)
	self.last = {}

    def reconnect(self):
	time.sleep(5);
	self.__init__();

    def handle_reply(self, prefix, code, params):
	if code == 1:
	    # join channels after welcome message
	    for channel in self.channels:
		self.join(channel)


    def handle_command(self, prefix, command, params):
	if command == "ERROR":
	    self.reconnect()
        
    def handle_quit(self, nick, reason):
	# Fishbot had quit, restart it.
	if nick == self.nick:
	    self.reconnect();

    def handle_say(self, source, to, message):
	# Target to reply to
	try:
	    # If the request was from a channel, reply to the channel.
	    self.channels.index(to)
	    respond = to
	except:
	    # If the request was from a private message, 
	    # reply to the private message.
	    respond = getnick(source)
	    
	if getnick(source) == "Y55":
	    return

	# Simple commands.
	if (message == "!fortune"):
	    for each in os.popen('fortune').readlines():
		self.say(respond, each)
	elif (message == "!sex"):
	    for each in os.popen('sex').readlines():
		self.say(respond, each)
	elif (re.search("\!help.*",message)):
	    self.say(respond, "!wiki coming soon. Try !google, !sex, !fortune, and url information today.")
	elif (re.search("\!s/.*/.*/",message)):
	    try:
		pattern = message.split('/')[1]
		repl = message.split('/')[2]
		self.say(respond, "%s meant to say: %s" % (getnick(source), re.sub(pattern, repl, self.last[getnick(source)])))
	    except:
		self.say(respond, "Invalid regular expression.")
	elif (re.search("\!upper .*", message)):
	    pass
	elif (message == "!list"):
	    # yay for a list
	    self.say(respond, "eggs")
	    self.say(respond, "beans")
	    self.say(respond, "five")
	    self.say(respond, "dentifrice")
	    self.say(respond, "macho nachos")
	    self.say(respond, "jam")
	elif (re.compile("^!wtf (.*)").search(message)):
	    # was insecure, now it's probably secure.
	    wtf = re.compile("^!wtf (.*)").search(message)
	    for each in os.popen('wtf ' + re.escape(wtf.group(1))).readlines():
		self.say(respond, (each or ("Gee... I don't know what " + wtf.group(1) + "means...")))
	elif (re.compile("^!google (.*)").search(message)):
	    # probably shouldn't be considered a simple command.
	    # maybe break this off into another function
	    google = re.compile("^!google (.*)").search(message)
	    # generate search URL
	    search_page = urllib.urlopen("http://www.google.com/search?hl=en&q="+ re.sub(" ", "+", google.group(1)) +"&btnG=Google+Search")
	    search_page = search_page.readlines()
	    for each in search_page:
		# wade through googles mass of html to pull out the first title
		# and url.
		if re.compile("<\!--m-->(.*?)<\/a>", re.M).search(each):
		    try:
			self.say(respond, "Google - '" + google.group(1) + "'| " + re.sub("<.*?>","",re.compile("<\!--m-->(.*?)<\/a>", re.M).search(each).group(1)) + " [ " + re.search("<\!--m-->.*?<a href=\"(.*?)\">", each, re.M).group(1) + " ]")
			return
		    except:
			self.say(respond, "Look it up yourself, Google sucks.")
			return
        p = self.moo.search(message)

	# This is sadly the original purpose of Fishbot. 
	# !google "not a real cowfish" for what little reasoning there is.
	if p:
	    self.say(respond, "LIEZ FISH GO MOO!")

	# The magic of URL parsing. 
	# I need to kill the number of try, except pairs I I used.
        m = self.re.search(message)
	if m:
	    try:
		resource = urllib.urlopen(m.group())
	    except:
		return
	    try:
		["application/xhtml+xml","text/html"].index(resource.info().getheader('Content-Type').split(';')[0])
	    except:
		try:
		    ["application/x-bittorrent"].index(resource.info().getheader('Content-Type').split(';')[0])
		    torrent = resource.readlines()
		    result = re.search("name[0-9]*?:(.*?)12:",torrent[0])
		    self.say(respond, "Torrent Name: " + result.group(1))
		except:
		    self.say(respond, "Content Type: " + (resource.info().getheader('Content-Type') or "b0rked webserver"))
		resource.close()
		return
	    try:
		xhtml = resource.readlines()
		dom = xml.dom.minidom.parseString(string.join(xhtml))
		self.say(respond, "XHTML, Title: " + getText(dom.getElementsByTagName("title")[0].childNodes))
	    except:
		for each in xhtml:
		    if re.compile("\<title.*\>(.*)\<\/title\>",re.I).search(each):
			match = re.search("\<title.*\>(.*)\<\/title\>",each,re.I)
			self.say(respond, "Malformed XML, Title: " + match.group(1))
	    resource.close()
	    return
	self.last[getnick(source)] = message

if __name__ == "__main__":
    # Spoof Firefox for the purposes of googling.
    urllib.URLopener.version = """Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.8) Gecko/20050609 Firefox/1.0.4"""
    bot = Y66()
    bot.mainloop()
