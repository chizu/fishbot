#!/usr/bin/python
"""Cookies are delicious delicacies."""
def handle_say(self, source, to, message):
    # self here is going to be the main Fishbot object
    respond = self.respond_to(source, to)
    
    if hasattr(self,'botsnack'):
        self.say(respond, "%d snacks received." % self.botsnack)
    else:
        self.say(respond, "I am hungry and poor without botsnacks.")
    
