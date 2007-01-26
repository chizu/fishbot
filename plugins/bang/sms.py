#!/usr/bin/python
"""An SMS module for fishbot.
All new sms'es will be announced within 10 seconds of arrival.
Commands are:
list - to list all sms'es
read <num> - print out message number <num>
del <num> - delete message number <num>
to <address> <message> - send an sms to <address>"""

import fishapi,imaplib,backend
from threading import Timer

announce = "#chshackers"

class address(backend.DatabaseObject):
    name = ""
    address = ""

def login():
    server = 'spicious.com'       #options for the script: mail server
    port = 993                    # port (this is for SSL)
    user = 'irc'                  #imap username
    passwd = 'SMS2ircw00t'        #imap password

    mc = imaplib.IMAP4_SSL(server, port)
    mc.login(user,passwd)
    mc.select()
    return mc

def timeout():
    outstr = []
    mc = login()
    typ, newmessages = mc.search(None, 'NEW')
    newmessages = newmessages[0].split()
    if len(newmessages) > 0:
        outstr.append("New SMS Arrived:")
        for mno in newmessages:
            typ, data = mc.fetch(mno, '(BODY[HEADER.FIELDS (SUBJECT FROM)] BODY[TEXT])')
            headers = data[0][1].split("\r\n")
            inAb = address(-1, address=headers[0].split()[1])
            if inAb:
                fromName = "From: " + inAb.name
            else:
                fromName = headers[0]
            outstr.append(fromName + "\n")
            outstr.append(headers[1])
            # Filter out footers, then split on newlines
            body = "\r\n".join(data[1][1].split("\r\n--\r\n")[:-1]).split("\r\n")
            for line in body:
                outstr.append(line)

        outstr = "\n".join(outstr)        
        fishapi.say(announce, outstr)
    
    t = Timer(10.0, timeout)
    t.start()

timeout()

def bang(pipein, arguments, event):
    import smtplib

    out_srv = 'smtp.comcast.net' #outgoing mail server
    src_add = 'irc@spicious.com'  #source email address ( for replies )

    arguments = arguments.split()

    if len(arguments) < 1:
        return("Please pass a command to !sms: list", None)


    if arguments[0] == 'list':
        outstr = []
        mc = login()
        typ, data = mc.search(None, 'ALL')
        outstr.append(str(len(data[0].split())) + " new messages:")
        for num in data[0].split():
            typ, data = mc.fetch(num, '(BODY[HEADER.FIELDS (SUBJECT FROM)])')
            headers = data[0][1].split("\r\n")
            outstr.append(num + " " + headers[0] + " " + headers[1])

        mc.logout()
        del(mc)
        return(outstr, None)

    if arguments[0] == 'read' and len(arguments) == 2:
        outstr = []
        mno = arguments[1]
        mc = login()
        typ, data = mc.fetch(mno, '(BODY[HEADER.FIELDS (SUBJECT FROM)] BODY[TEXT])')
        if typ == 'NO':
            return("Error fetching message", None)
        outstr.append("Message " + mno)
        headers = data[0][1].split("\r\n")
        inAb = address(-1, address=headers[0].split()[1])
        if inAb:
            fromStuff = "From: " + inAb.name
        else:
            fromStuff = headers[0]
        outstr.append(fromStuff + "\n")
        outstr.append(headers[1])
        # Filter out footers, then split on newlines
        body = "\r\n".join(data[1][1].split("\r\n--\r\n")[:-1]).split("\r\n")
        for line in body:
            outstr.append(line)
        mc.close()
        mc.logout()
        del(mc)
        if len(outstr) > 1024:
            return ("Message length exceeded, " + str(len(outstr) - 1024) + " characters too long.", None)
        else:
            return(outstr, None)

    if arguments[0] == 'del' and len(arguments) == 2:
        outstr = []
        mno = arguments[1]
        mc = login()
        typ, data = mc.store(mno, '+FLAGS', '\\Deleted')
        if typ == 'OK':
            outstr.append("Message " + mno + " successfully deleted.")
        mc.expunge()
        mc.close()
        mc.logout()
        del(mc)
        return(outstr, None)

    if arguments[0] == 'check':
        return(outstr, None)

    if arguments[0] == 'to' and len(arguments) > 2:
        out_add = address(-1, name=arguments[1])

        if out_add:
            to = out_add.address
        else:
            to = arguments[1]
        
        message = "From: " + src_add + "\r\n"
        message += "To: " + to + "\r\n"
        message += "Subject: " + event._target + " " + event._source.split('!')[0] + "\r\n\r\n"
        message += " ".join(arguments[2:])
        mc = smtplib.SMTP(out_srv)
        mc.sendmail(src_add, to, message)
        mc.quit()
        del(mc)
        return("SMS successfully sent.", None)
        
        
