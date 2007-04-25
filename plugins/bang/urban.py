#!/usr/bin/python
"""Look up a word in the Urban Dictionary.
!urban word"""

def bang(pipein, arguments, event):
    import SOAPpy

    server = SOAPpy.SOAPProxy("http://api.urbandictionary.com/soap")
    urban = server.lookup("7df8eccad5391dbbb45e81fa77f4c1a8", arguments)

    if len(urban) > 1:
        if(len(urban[0].definition) < 256):
            return (arguments + ": " + urban[0].definition + "\n", None)
        else:
            return (urban[0].url, None)

    return ("Could not find a definition for " + arguments + "\n", None)
    
