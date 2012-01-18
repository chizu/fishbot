#!/usr/bin/python
"""!grep - Search for strings!
Usage: <text> | !grep <search string>"""
import re,os,getopt,string

def bang(pipein, arguments, event):
    command = 'grep ' + re.escape(arguments) + \
        ' <<EOF\n' + pipein.replace('EOF', 'No cheating.') + \
        '\nEOF'
    print command
    return (os.popen(command).readlines(), None)
