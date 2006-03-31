#!/usr/bin/python
import sys,string

def handle_say(self, source, to, message):
    respond = self.respond_to(source, to)
    try:
	if len(message.split()) >= 2:
            query = string.join(message.split()[1:])
            results = self.backend.sql_query(query)
            if len(results) > 6:
                self.say(respond, "Query returned %s rows." % len(results))
            else:
                for each in results:
                    self.say(respond, str(each))
    except:
	self.say(respond, "Incorrect query syntax.")
	raise
