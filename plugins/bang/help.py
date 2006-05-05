#!/usr/bin/python
"""!help - Help with fishbot commands.
Usage: !help <command>"""
import string
import plugins.bang
import importer
import fishapi

def bang(pipein, arguments, event):
    if len(arguments) is 0:
        return (fishapi.version + ". Available commands are: !" + string.join(plugins.bang.__all__,', !') + ".", None)
    else:
        reply = []
        for each in arguments.split():
            try:
                if each[0] is "!":
                    each = each[1:]
                help_string = importer.__import__(each, globals(), locals(), 'plugins/bang').__doc__
                reply.append(help_string)
            except:
                reply.append("No help available for %s." % each)
                raise
        return (reply, None)
    
