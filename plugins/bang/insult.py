#!/usr/bin/python
import fishapi,string,re

def bang(pipein, arguments, event):
    groups = fishapi.http_grep("http://www.webweaving.org/", '(Thou\s[^\n]*)')
    if groups:
        insult = groups[0]
        return ((arguments or pipein) + ", " + insult + "!", None)
