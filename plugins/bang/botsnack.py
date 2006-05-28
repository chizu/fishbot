#!/usr/bin/python
"""Cookies are delicious delicacies."""
def bang(pipein, arguments, event):
    if event.source()[0:6] == "Sauce!":
        return
    else:
        return (":)", None)
