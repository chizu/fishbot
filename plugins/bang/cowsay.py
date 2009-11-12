#!/usr/bin/python
"""!cowsay - The cow shall speak!
Usage: <text> | !cowsay -f <cowfile>"""
import re,os,getopt,string

def bang(pipein, arguments, event):
    cowfile = ''
    options, args = getopt.getopt(arguments.split(), 'f:')
    for each in options:
        if each[0] == '-f':
            cowfile = '-f ' + each[1]
    cowsay = pipein or string.join(args) or "Mooo"
    # Fish go moo!
    if re.search('moo', cowsay, re.I) or '-- --- ---' in cowsay:
        cowfile = '-f ' + 'fish'
    output = os.popen('cowsay ' + cowfile + " " + re.escape(cowsay)).readlines()
    return ([x.rstrip() for x in output], None)
