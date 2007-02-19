#!/usr/bin/env python
"""Simple SMS/Email interface client."""
import generic, imaplib, datetime

class MailEvent(generic.Event):
    """Mail or SMS event."""
    pass

class Client(generic.Client):
    """SMS/Mail server interface. This is the main class, which will behave like a normal protocol plugin."""
    protocol = "mail"
    def __init__(self, emailaddr, hostname, port, username=None, password=None, ssl=False, tick=120):
        self.emailaddr = emailaddr
        self.host = hostname
        self.port = port
        self.username = username
        self.password = password
        self.ssl = ssl
        self.channels = None
        self.connected = False
        self.mailc = None
        self.server = None
        self.tick = tick
        self.triggers.register("incoming", self.incoming)
        self.connect()
        

    def connect(self):
        if not self.connected:
            if self.ssl:
                self.mailc = imaplib.IMAP4_SSL(self.host, self.port)
            else:
                self.mailc = imaplib.IMAP4(self.host, self.port)
  
            if self.mailc.login(self.username, self.password)[0] == 'OK':
                self.mailc.select()
                self.connected = True
            else:
                self.mailc.logout()
                del(self.mailc)
        
    def disconnect(self):
        if self.connected:
            self.mailc.logout()
            del(self.mailc)
            self.connected = False

    def message(self, to, message, event):
        """This is the send function"""

        
    def incoming(self, event):
        """This will be overriden depending on the type of client"""

    def poll(self):
        import time
        while 1:
            time.sleep(self.tick)
            if self.connected:
                print "Checking for new messages"
                if self.mailc.recent() != None:
                    typ, newmessages = self.mailc.search(None, 'UNSEEN')
                    print newmessages
                    newmessages = newmessages[0].split()
                    for mno in newmessages:
                        typ, data = self.mailc.fetch(mno, '(BODY[HEADER.FIELDS (SUBJECT FROM)] BODY[TEXT])')
                        headers = data[0][1].split("\r\n")
                        event = MailEvent(self, headers[0], headers[1], 'incoming', data[1])
                        self.triggers.trigger(event.command, event)
                        yield None


class ForwardClient(Client):
    """A special client class that just forwards messages to a list of channels"""

    def attach(self, ircserver=None, channels=None):
        self.server = ircserver
        self.channels = channels


    def incoming(self, event):
        import backend
        out = ""
        class address(backend.DatabaseObject):
            name = ""
            address = ""

        inAb = address(-1, address=event.source.split()[1])
        if inAb:
            fromName = "From " + inAb.name
        else:
            fromName = event.source

        out += "New Message " + fromName + "\n"
        out += event.target + "\n"
        out += event.params[1]

        if self.server != None and self.channels != None:
            for channel in self.channels:
                self.server.say(channel, out)

        
