#!/usr/bin/python
"""Plugin management."""
import importer
import re
from glob import glob

expressions = {}

submodules = glob("plugins/*")
__all__ = set()
for each in submodules:
    each = each.split('/')[-1].split('.')[0]
    __all__.add(each)
__all__.remove('__init__')

for each in __all__:
    module = importer.__import__(name=each, path="plugins")
    expressions[re.compile(module.expression[0])] = module.expression[1]
