#!/usr/bin/python
"""!echo - Echo things
Usage: !echo <text>"""
def bang(pipein, arguments, event):
    return (pipein + arguments or "Mooo", None)
