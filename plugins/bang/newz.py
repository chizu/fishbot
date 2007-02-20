#!/usr/bin/env python
"""NewzBin search for fishbot:
!newz [-n <num>] [-c <cat>] search
Where num is the number of results to return, and cat is a newzbin category."""

def bang(pipein, arguments, event):
    import newzlib
    
    arguments = arguments.split()
    
    if arguments[0] == '-n':
        num = int(arguments[1])
        if num > 10:
            num = 10
        arguments = arguments[2:]
    else:
        num = 2

    if arguments[0] == '-c':
        cat = arguments[1]
        arguments = arguments[2:]
    else:
        cat = 'all'

    search = ' '.join(arguments)
    nz = newzlib.Newz()

    res = nz.search(search, category=cat)
    if res:
        out = []

        for line in res[:num]:
            out.append(line[2] + ': ' + line[3])

        return(out, None)
    else:
        return('No results', None)
