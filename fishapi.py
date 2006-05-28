#!/usr/bin/python
import importer, time
import sys, os

version = "Fishbot 3.0 - Beta"
#execution_time - set by main class
#fishbot - set by main class

def halt(message):
    fishbot.disconnect(message)
    sys.exit(0)

def restart(message):
    fishbot.disconnect(message)
    os.execv(sys.argv[0], sys.argv[1:])
    sys.exit(0)
