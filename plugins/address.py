#!/usr/bin/python
"""Execute !<command> code when '<nickname> <command>' is said."""
def address(self, event):
    import re, bang
    prefix = "^\s*" + self.connection.get_nickname() + "\W+"
    if len(event.arguments()) > 0 and re.search(prefix, event.arguments()[0]):
        event.arguments()[0] = re.sub(prefix, "!", event.arguments()[0])
        bang.bang(self, event)

expression = ('.*', address)
