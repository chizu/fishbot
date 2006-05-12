#!/usr/bin/python
import re,os,random

def bang(pipein, arguments, event):
    if arguments:
	roll = int(arguments)
    else:
        roll = 20
    return (str(random.randint(1,roll)),None)
