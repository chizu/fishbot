#!/usr/bin/python
"""An SMS module for fishbot.  This mostly acts as a mail relay."""

import fishapi,imaplib
from threading import Timer

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
            outstr.append(headers[0])
            outstr.append(headers[1])
            body = data[1][1].split("\r\n")
            body = data[1][1].split("\r\n")
            for line in body:
                outstr.append(line)

        outstr = "\n".join(outstr)        
        fishapi.say('#chshackers', outstr)
    t = Timer(10.0, timeout)
    t.start()

timeout()

def bang(pipein, arguments, event):
    import smtplib
    out_srv = 'smtp.comcast.net' #outgoing mail server
    src_add = 'irc@spicious.com'  #source email address ( for replies )

    arguments = arguments.split()

    if len(arguments) < 1:
        return("Please pass a command to !sms: list")

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
        outstr.append(headers[0])
        outstr.append(headers[1])
        body = data[1][1].split("\r\n")
        for line in body:
            outstr.append(line)
        mc.close()
        mc.logout()
        del(mc)
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
        to = arguments[1]
        message = "From: " + src_add + "\r\n"
        message += "To: " + to + "\r\n"
        message += "Subject: " + event._target + "\r\n"
        message += " ".join(arguments[2:])
        print message
        mc = smtplib.SMTP(out_srv)
        mc.sendmail(src_add, to, message)
        mc.quit()
        del(mc)
        return("SMS successfully sent.", None)
