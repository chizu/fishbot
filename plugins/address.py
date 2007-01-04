#!/usr/bin/python
"""Execute !<command> code when '<nickname> <command>' is said."""
def address(self, event):
    import re, plugins.bang
    prefix = "^\b" + self.connection.get_nickname()
    if re.search(prefix, event.arguments()[0]):
        event.arguments()[0] = re.sub(prefix, event.arguments()[0], "!")
        bang.bang(self, event)

expression = ('.*\?\b*$', questions)
