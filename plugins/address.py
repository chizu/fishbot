#!/usr/bin/python
"""Execute !<command> code when '<nickname> <command>' is said."""
def address(self, event):
    import re, plugins.bang
    prefix = "^\s*" + self.connection.get_nickname() + "\W+"
    print prefix
    if re.search(prefix, event.arguments()[0]):
        print event.arguments()[0]
        event.arguments()[0] = re.sub(prefix, "!", event.arguments()[0])
        print event.arguments()[0]
        plugins.bang.bang(self, event)

expression = ('.*', address)
