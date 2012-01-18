#!/usr/bin/python
"""Look up a word in the Urban Dictionary. Optionally use n'th entry.
!urban [<n>] <word>"""

def bang(pipein, arguments, event):
    import SOAPpy
    import re

    match = re.compile("^(\d+) (.*)").match(arguments)
    if not match:
        num = 0
    else:
        (num, arguments) = match.groups()

    server = SOAPpy.SOAPProxy("http://api.urbandictionary.com/soap")
    urban = server.lookup("7df8eccad5391dbbb45e81fa77f4c1a8", arguments)

    if len(urban) > 1:
        return (urban[num].definition.replace("\n\n", "\n").split("\n"), None)

    return ("Could not find a definition for " + arguments + "\n", None)
