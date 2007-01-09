#!/usr/bin/python
"""Example Fishbot script."""
from fishbot import Fishbot

bot = Fishbot(server = "irc.chshackers.com", channels = ["#chshackers", "#mmo-dev"])
bot.start()
