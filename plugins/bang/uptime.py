#!/usr/bin/python
"""!uptime - Report uptime."""
import fishapi,time

def bang(pipein, arguments, event):
    return (str(int(time.time() - fishapi.execution_time)) + " seconds", None)
