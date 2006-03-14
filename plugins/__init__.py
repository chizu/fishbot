#!/usr/bin/python
"""Store regexp patterns and the reactions for them.

This should be a priority dictionary named expressions."""

def bang(self, event):
    import re
    import importer
    match = re.search('^\!(\w+).*$', event.arguments()[0])
    if match:
        try:
            module = importer.__import__(match.group(1), globals(), locals(), 'bang')
            if module:
                module.handle_say(self, event.source(), event.target(), event.arguments()[0])
        except ImportError:
            return
        except:
            raise

expressions = {
    '^\!(\w+).*$':bang
}

