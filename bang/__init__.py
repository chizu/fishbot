#!/usr/bin/python
import sys
from glob import glob
__all__ = [each.split('/')[1].split('.')[0] \
	   for each in glob('bang/*.py')]
__all__.remove('__init__')

class BangCommand(dict):
    """A package containing dynamically reloadable modules."""
    def __init__(self):
	for each in __all__:
	    self + each
	
    def __add__(self, name):
	self[name] = getattr(__import__('bang.' + name), name)

    def __sub__(self, name):
	del(self[name])
	del(sys.modules["bang.%s" % name])
