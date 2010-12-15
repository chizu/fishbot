#!/usr/bin/env python
"""Example Fishbot script."""
from fishbot import Fishbot
import protocols.irc

def oper(server, username, password):
	server.oper(username, password)

bot = Fishbot({"chshackers":protocols.irc.Client(nick="Fishbot", realname="Fishbot", hostname="irc.chshackers.com", port=6667)})
# Oper example
bot.servers["chshackers"].triggers.register("001", oper, (bot.servers["chshackers"], "username", "password"))
bot.servers["chshackers"].join("#chshackers")
bot.start()
