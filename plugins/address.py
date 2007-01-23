#!/usr/bin/python
"""Execute !<command> code when '<nickname> <command>' is said."""
def address(self, event):
    import re, bang, copy
    prefix = "^\s*" + self.connection.get_nickname() + "\W+"
    if len(event.arguments()) > 0 and re.search(prefix, event.arguments()[0]):
        bang_event = copy.deepcopy(event)
        bang_event.arguments()[0] = re.sub(prefix, "!", bang_event.arguments()[0])
        bang.bang(self, bang_event)
    
expression = ("", address)
