import sqlobject
import sys, os

connect_string = "sqlite:" + os.getcwd() + sys.argv[0].split('/')[1] + ".sqlite"
sqlobject.sqlhub.processConnnection = sqlobject.connectionForURI(connect_string)

class Message(sqlobject.SQLObject):
    source = sqlobject.UnicodeCol()
    target = sqlobject.UnicodeCol()
    message = sqlobject.UnicodeCol()
    message_time = sqlobject.DateTimeCol()
    raw = sqlobject.UnicodeCol(default = None)


print "init"
#Message.createTable()
