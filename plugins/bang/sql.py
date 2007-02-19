#!/usr/bin/python
import sys,string
import psycopg2
con = psycopg2.connect(user='fishbotread', host='localhost', database='fishbot')

def bang(pipein, arguments, event):
    query = arguments or pipein
	cur = con.cur()
    try:
		cur.execute(query)
		cur.connection.commit()
        results = cursor.fetchall()
		cur.close()
        if len(results) > 6:
            return ("Query returned %s rows." % len(results), None)
        else:
            values = []
            for each in results:
                values.append(str(each))
            return (values, None)
    except:
		cur.connection.rollback()
		cur.close()
		raise
