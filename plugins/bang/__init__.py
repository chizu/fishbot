#!/usr/bin/python
import sys, string
from glob import glob
submodules = glob("plugins/bang/*")
__all__ = set()
for each in submodules:
    each = each.split('/')[-1].split('.')[0]
    __all__.add(each)
__all__.remove('__init__')

def bang(self, event):
    # Early exit for spam.
    #if self.last[self.getnick(event.source())][0] == event.arguments()[0]:
    #    return
    import re
    import importer
    import irclib
    pipes = [string.strip(i) for i in event.arguments()[0].split('|')]
    pipein = ""
    for pipe in pipes:
        if pipe:
            name = re.search(expression[0], pipe).group(1)
            arguments = string.strip(re.search(expression[0], pipe).group(2))
            try:
                module = importer.__import__(name, globals(), locals(), 'plugins/bang')
                if hasattr(module, 'bang'):
                    # New API
                    if event.target() in self.channels:
                        respond = event.target() # Reply to the channel
                    else:
                        respond = irclib.nm_to_n(event.source()) # Private message

                    (pubmsg, action) = module.bang(pipein, arguments, event)
                    if pubmsg and pipe is pipes[-1]:
                        if isinstance(pubmsg, (list, tuple)):
                            for each in pubmsg:
                                for each in each.split('\n'):
                                    self.connection.privmsg(respond, each)
                        else:
                            self.connection.privmsg(respond, pubmsg)
                    elif pubmsg:
                        if isinstance(pubmsg, (list, tuple)):
                            pipein = string.join(pubmsg)
                        else:
                            pipein = pubmsg
                    if action:
                        if isinstance(action, list):
                            for each in action:
                                self.connection.ctcp("ACTION", to, each)
                        else:
                            self.connection.ctcp("ACTION", to, action)

                elif hasattr(module, 'handle_say'):
                    # Old API
                    module.handle_say(self, event.source(), event.target(), event.arguments()[0])
            except ImportError:
                return
            except:
                raise

expression = ("^\!(\w+)(.*)$", bang)
