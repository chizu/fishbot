#!/usr/bin/python
import sys
from glob import glob
submodules = glob("plugins/bang/*")
__all__ = set()
for each in submodules:
    each = each.split('/')[-1].split('.')[0]
    __all__.add(each)
__all__.remove('__init__')

def bang(self, event):
    # Early exit for spam.
    if self.last[self.getnick(event.source())][0] == event.arguments()[0]:
        return
    import re
    import importer
    match = re.search(expression[0], event.arguments()[0])
    if match:
        try:
            module = importer.__import__(match.group(1), globals(), locals(), 'plugins/bang')
            if module:
                module.handle_say(self, event.source(), event.target(), event.arguments()[0])
        except ImportError:
            return
        except:
            raise

expression = ("^\!(\w+).*$", bang)
