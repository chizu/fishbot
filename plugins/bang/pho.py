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

def bang(pipein, arguments, event):
    response = ""
    if pipein:
	for each in pipein:
	    try:
		response += pho[each.lower()] + " "
	    except KeyError:
		pass
    return (response, None)
