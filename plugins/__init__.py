#!/usr/bin/python
"""Plugin management."""
import importer
import re
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
    expression = re.compile(module.expression[0])
    if expressions.has_key(expression):
        expressions[expression].append(module.expression[1])
    else:
        expressions[expression] = [module.expression[1]]
