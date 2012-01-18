#!/usr/bin/python
"""Fishbot Plugins

Top level of the plugin tree. In general, if you're writing a Fishbot add-on, it should be a child of this package.

Plugins are fairly simple, they have only one required component. A plugin is anything with the property expression that is a tuple with a regular expression and a function call.

A plugin that does nothing would be,
>>> def do_nothing(self, event): pass
>>> expression=('', do_nothing)
Which says to Fishbot 'When the empty regular expression is encountered, execute the pass function.'

The regular expression can be anything parsable by the python re module. These are checked in alphabetical order (according to the plugin filename) and executed when they match.

The function can be any python function that accepts the arguments (self, event) where self is the Fishbot object, and event is the irclib event that triggered this function.

For a more complete working example, see the cowsgomoo.py plugin.
"""
import importer, threading
from glob import glob

expressions = {}

submodules = glob("plugins/*")
submodules.sort()
__all__ = set()
for each in submodules:
    each = each.split('/')[-1].split('.')[0]
    __all__.add(each)
__all__.remove('__init__')
__all__ = list(__all__)
__all__.sort()

for each in __all__:
    module = importer.__import__(name=each, path="plugins")
    expression = module.expression[0]
    if expression in expressions:
        expressions[expression].append(module.expression[1])
    else:
        expressions[expression] = [module.expression[1]]

class PluginThread(threading.Thread):
    def __init__(self, func, args):
        self.func = func
        self.args = args
        super(PluginThread, self).__init__()

    def run(self):
        self.func(*self.args)
