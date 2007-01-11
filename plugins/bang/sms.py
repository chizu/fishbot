#!/usr/bin/python
"""An SMS module for fishbot.  This mostly acts as a mail relay."""

def bang(pipein, arguments, event):
    import imaplib
    from threading import Timer
    server = 'spicious.com' #options for the script: mail server
    port = 993 # port (this is for SSL)
    user = 'irc'
    passwd = 'SMS2ircw00t'

    def login():
        mc = imaplib.IMAP4_SSL(server, port)
        mc.login(user,passwd)
        mc.select()
        return mc

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
        return(outstr, None)
