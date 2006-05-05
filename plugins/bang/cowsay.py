#!/usr/bin/python
"""!cowsay - The cow shall speak!
Usage: <text> | !cowsay"""
import re,os

def bang(pipein, arguments, event):
    cowsay = pipein or arguments
    return (os.popen('cowsay ' + re.escape(cowsay)).readlines(), None)

