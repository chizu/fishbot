#!/usr/bin/env python
"""Addressbook Plugin"""

def bang(pipein, arguments, event):
    import fishapi

    arguments = arguments.split()

    class address(fishapi.DatabaseObject):
        name = ""
        address = ""

    if arguments[0] == 'add' and len(arguments) == 3:
        addr = address(-1, name = '^' + arguments[1] + '$', address = '^' + arguments[2] + '$')

        if len(addr) > 0:
            outstr = "Replacing " + addr.name
        else:
            outstr = "Added"
        addr = address(name = arguments[1], address = arguments[2])
        return(outstr, None)

    if arguments[0] == 'find' and len(arguments) == 2:
        outstr = []
        addrs = address(-1, name = arguments[1] + " OR address ~ '" arguments[1] "'")

        for each in addr:
            outstr.append("[" + each.id + "] "+ each.name + " - " + each.address)

        return(outstr, None)
