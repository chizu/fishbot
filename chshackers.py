#!/usr/bin/python
"""Example Fishbot script."""
from fishbot import Fishbot

bot = Fishbot(server = "irc.chshackers.com", channels = ["#chshackers", "#mmo-dev"])
#bot.oper = {'username':'fishbot', 'password':''} # Have Fishbot oper before joining channels
bot.start()
