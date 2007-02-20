#!/usr/bin/env python
"""NewzBin search for fishbot:
!newz [-n <num>] search
Where num is the number of results to return."""

def bang(pipein, arguments, event):
    import newzlib
    
    arguments = arguments.split()

    if arguments[0] == '-n':
        num = str(arguments[1])
        if num > 10:
            num = 10
        search = ' '.join(arguments[2:])
    else:
        num = 2
        search = ' '.join(arguments)

    nz = newzlib.Newz()

    res = nz.search(search)

    out = []

    for line in res[:num]:
        out.append(line[2] + ': ' + line[3])

    return(out, None)
