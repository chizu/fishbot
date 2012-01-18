#!/usr/bin/python
"""Execute !<command> code when '<nickname> <command>' is said."""
def address(self, event):
	import re, bang, copy
	prefix = "^\s*" + event.server.nick + "\W+"
	if len(event.arguments) > 0 and re.search(prefix, event.arguments):
		bang_event = copy.copy(event)
		bang_event.arguments = re.sub(prefix, "!", bang_event.arguments)
		bang.bang(self, bang_event)

expression = ("", address)
