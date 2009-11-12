#!/usr/bin/python
"""Bang(!) command plugins

This Fishbot plugin in turn implements it's own plugin system. These are simple, and if you want to make a new Fishbot command in the style of "!<something> arguments" you should make one of these.

These plugins are just a normal python module. Any python code can go in these plugins. Suppose you have a file named 'hello.py'. A simple example would be:

def bang(pipein, arguments, event):
	return ("Hello world.", None)

This would cause Fishbot to say "Hello world." when it saw !hello on a channel.

That's the basic idea. Other things to know are, pipein contains anything piped in to your command (!echo test | !hello, and pipein would contain the string "test"), arguments is anything following the command (!hello world, and arguments will have the string " world" in it), and event is an IRCEvent for information on who/what said !hello in the first place.

("Hello world.", None) tells Fishbot to say something to the source of command. If you wanted it to do /me "Hello World" it would be (None, "Hello World").

Fishapi is probably also useful if you want to do anything more than trivial. See its documentation for using it.
"""
import sys, string
from glob import glob
submodules = glob("plugins/bang/*")
__all__ = set()
for each in submodules:
	each = each.split('/')[-1].split('.')[0]
	__all__.add(each)
__all__.remove('__init__')

def bang(self, event):
	import re
	import importer
	pipes = [string.strip(i) for i in event.arguments.split('|')]
	pipein = ""
	for pipe in pipes:
		if pipe:
			postpipe = re.search(expression[0], pipe)
			if not postpipe:
				# invalid bang command syntax
				print "bang: invalid syntax - '" + pipe + "'"
				return
			name = postpipe.group(1)
			arguments = string.strip(postpipe.group(2))
			try:
				module = importer.__import__(name, globals(), locals(), 'plugins/bang')
				if hasattr(module, 'bang'):
					# New API
					respond = self.respond_to(event.source, event.target)
					(pubmsg, action) = module.bang(pipein, arguments, event)
					if pubmsg and pipe is pipes[-1]:
						if isinstance(pubmsg, (list, tuple)):
							lines = list()
							for line in pubmsg:
								lines += line.split('\n')
						else:
							lines = pubmsg.split('\n')
						if len(lines) > 5:
							# Private message
							respond = self.respond_to(event.target, event.source)
						for each in lines:
							if each != '':
								event.server.message(respond, each)
					elif pubmsg:
						if isinstance(pubmsg, (list, tuple)):
							pipein = string.join(pubmsg, '\n')
						else:
							pipein = pubmsg
					if action:
						if isinstance(action, (list, tuple)):
							for each in action:
								event.server.action(respond, each)
						else:
							event.server.action(respond, action)

				elif hasattr(module, 'handle_say'):
					# Old API
					module.handle_say(self, event.source, event.target, event.arguments)
			except ImportError:
				return
			except:
				raise

expression = ("^\!(\w+)(.*)$", bang)
