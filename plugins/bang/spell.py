#!/usr/bin/python
"""!spell - Spellcheck your last line, or anything passed to !spell.
Usage: !spell, !spell <text>, or <text> | !spell"""
import os,re
import backend

def bang(pipein, arguments, event):
    if pipein or arguments:
        spelling = [pipein or arguments]
    else:
        result = backend.last(type(event), event.source, 2)
        spelling = [result[1].arguments]
    reply = []
    for spell in spelling:
        for each in os.popen('echo %s | aspell -a' % re.escape(spell)).readlines():
            for each in each.split("\n"):
                if len(each) > 0 and each[0] == '&':
                    reply.append(each)
    return (reply, None)
