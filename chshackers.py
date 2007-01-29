#!/usr/bin/python
"""Example Fishbot script."""
from fishbot import Fishbot
import protocols

def oper(server, username, password):
	server.oper(username, password)

bot = Fishbot({"chshackers":protocols.irc.Client(nick="Fishbot", realname="Fishbot", hostname="grandpa.chshackers.com", port=6667)})
# Oper on chshackers
bot.servers["chshackers"].triggers.register("001", oper, (bot.servers["chshackers"], "chizu", "peanutbutter"))
bot.servers["chshackers"].join("#chshackers")
bot.servers["chshackers"].join("#mmo-dev")
bot.start()
