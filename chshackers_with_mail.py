#!/usr/bin/env python
"""Example Fishbot script."""
from fishbot import Fishbot
import protocols.irc, protocols.mail

def oper(server, username, password):
	server.oper(username, password)

bot = Fishbot({
	"chshackers":protocols.irc.Client(nick="testdummy",
					  realname="Fishbot-Kev",
					  hostname="grandpa.chshackers.com",
					  port=6667),
	"mail":protocols.mail.ForwardClient(emailaddr="irc@spicious.com",
					    hostname="spicious.com",
					    port=993, username='irc',
					    password='SMS2ircw00t',
					    ssl=True,
					    tick=10)
	})
bot.servers["chshackers"].join("#test")
bot.servers["mail"].attach(bot.servers["chshackers"], ["#test"])
bot.start()
