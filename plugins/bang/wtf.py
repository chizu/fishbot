#!/usr/bin/python
import re,os

def bang(pipein, arguments, event):
    respond = []
    if arguments:
	for each in os.popen('wtf ' + re.escape(arguments)):
	    respond.append((each or ("Gee... I don't know what " + arguments + "means...")))
    return (respond, None)
