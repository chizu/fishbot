#!/usr/bin/python
import re

pho = {'a':'Alpha',
       'b':'Bravo',
       'c':'Charlie',
       'd':'Delta',
       'e':'Echo',
       'f':'Foxtrot',
       'g':'Golf',
       'h':'Hotel',
       'i':'India',
       'j':'Juliet',
       'k':'Kilo',
       'l':'Lima',
       'm':'Mike',
       'n':'November',
       'o':'Oscar',
       'p':'Papa',
       'q':'Quebec',
       'r':'Romeo',
       's':'Sierra',
       't':'Tango',
       'u':'Uniform',
       'v':'Victor',
       'w':'Whiskey',
       'x':'X-ray',
       'y':'Yankee',
       'z':'Zulu',
       '0':'Zero',
       '1':'One',
       '2':'Two',
       '3':'Three',
       '4':'Four',
       '5':'Five',
       '6':'Six',
       '7':'Seven',
       '8':'Eight',
       '9':'Nine'
       }

def handle_say(self, source, to, message):
    respond = self.respond_to(source, to)
    response = ""
    arg = re.search('^!pho (.*)$', message)
    if arg:
	arg = arg.group(1)
	for each in arg:
	    try:
		response += pho[each.lower()] + " "
	    except KeyError:
		pass
	self.say(respond, response)
