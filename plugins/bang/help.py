#!/usr/bin/python
"""!help - Help with fishbot commands.
Usage: !help <command>"""
import string
import plugins.bang
import importer

def handle_say(self, source, to, message):
    respond = self.respond_to(source, to)
    if len(message.split()) is 1:
        self.say(respond, self.version + ". Available commands are: !" + string.join(plugins.bang.__all__,', !') + ".")
    else:
        for each in message.split()[1:]:            
            try:
                if each[0] is "!":
                    each = each[1:]
                help_string = importer.__import__(each, globals(), locals(), 'plugins/bang').__doc__
                self.say(respond, help_string)
            except:
                self.say(respond, "No help available for %s." % each)
                raise
