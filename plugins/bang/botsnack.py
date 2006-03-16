#!/usr/bin/python
"""Cookies are delicious delicacies."""
def handle_say(self, source, to, message):
    # self here is going to be the main Fishbot object
    respond = self.respond_to(source, to)
    
    if hasattr(self,'botsnack'):
        self.botsnack += 1
    else:
        self.botsnack = 1
    
    self.say(respond, ":)")
