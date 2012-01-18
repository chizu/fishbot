#!/usr/bin/env python
"""Example Fishbot script."""
from fishbot import Fishbot
import protocols.irc

def identify(server, password):
    server.message("nickserv", "identify {0}".format(password))

def oper(server, username, password):
    server.oper(username, password)

bot = Fishbot({"example":protocols.irc.Client(nick="Fishbot", realname="Fishbot", hostname="irc.example.com", port=6667)})
# Oper example
bot.servers["example"].triggers.register("001", oper, (bot.servers["example"], "username", "password"))
bot.servers["example"].triggers.register("001", identify, (bot.servers["example"], "ident-password"))
bot.servers["example"].join("#example")
bot.start()
