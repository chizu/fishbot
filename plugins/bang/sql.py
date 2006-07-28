#!/usr/bin/python
import sys,string,traceback,fishapi

def bang(pipein, arguments, event):
    query = arguments or pipein
    try:
        results = fishapi.backend.sql_query(query)
        if len(results) > 6:
            return ("Query returned %s rows." % len(results), None)
        else:
            values = ""
            for each in results:
                values += str(each)
            return (values, None)
    except:
	raise
        return (traceback.format_exc(1), None)
