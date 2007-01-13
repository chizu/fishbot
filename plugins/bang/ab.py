#!/usr/bin/env python
"""Addressbook Plugin"""

def bang(pipein, arguments, event):
    import backend

    arguments = arguments.split()

    if len(arguments) < 1:
        return("Please give ab a command", None)

    class address(backend.DatabaseObject):
        name = ""
        address = ""

    if arguments[0] == 'add' and len(arguments) == 3:
        addr = address(-1, name = arguments[1], address = arguments[2]  )

        if len(addr) > 0:
            outstr = "Replacing " + addr.name
        else:
            outstr = "Added"
        addr = address(name = arguments[1], address = arguments[2])
        return(outstr, None)

    elif (arguments[0] == 'find' and len(arguments) == 2) or arguments[0] == 'list':
        outstr = []
        
        if arguments[0] == 'find':
            addrs = address(-1, name = arguments[1] + "' OR address ~ '" + arguments[1])
        else:
            addrs = address(-1)

        print addrs
            
        for each in addrs:
            outstr.append("[" + str(each.id) + "] "+ each.name + " - " + each.address)

        return(outstr, None)

    return(None, None)
