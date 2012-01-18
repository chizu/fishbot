#!/usr/bin/env python
"""!karma - Show karma stats for things.
!karma <thing> | stats [[top,bottom,middle] <n>]"""
from operator import itemgetter

import backend
import fishapi
from plugins.karma import Karma

stats_sql = """SELECT COALESCE(positive.string, negative.string) AS string, 
COALESCE(positive.final_score, 0) + COALESCE(negative.final_score, 0) AS score 
FROM 
  (SELECT scores.string, scores.total * people.total 
   AS final_score 
   FROM 
    (SELECT string, 
     sum(score) as total 
     FROM karma 
     WHERE score > 0 
     GROUP BY string 
     ORDER BY sum(score)) AS scores 
   JOIN 
    (SELECT string, 
     count(nick) as total 
     FROM karma 
     WHERE score > 0 
     GROUP BY string 
     ORDER BY sum(score)) AS people 
   ON scores.string = people.string 
   ORDER BY final_score) AS positive 
FULL OUTER JOIN 
  (SELECT scores.string, scores.total * people.total
   AS final_score 
   FROM 
    (SELECT string, 
     sum(score) as total 
     FROM karma 
     WHERE score < 0 
     GROUP BY string 
     ORDER BY sum(score)) AS scores 
   JOIN 
    (SELECT string, 
     count(nick) as total 
     FROM karma
     WHERE score < 0 
     GROUP BY string 
     ORDER BY sum(score)) AS people 
   ON scores.string = people.string 
   ORDER BY final_score) AS negative 
ON positive.string = negative.string
ORDER BY score;"""

def calckarma(thing):
    pcount = 0
    positive = 0
    ncount = 0
    negative = 0
    for each in thing:
        score = each.score
        if score < 0:
            ncount += 1
            negative += abs(score)
        elif score > 0:
            pcount += 1
            positive += score
    return (positive * pcount) - (negative * ncount)

def bang(pipein, arguments, event):
    sql_session = backend.get_session()
    token = arguments.strip().lower()
    if not token:
        token = fishapi.getnick(event.source).strip().lower()
        arguments = token
    tokens = token.split()
    if tokens[0] == 'stats':
        results = sql_session.query("string", "score").\
            from_statement(stats_sql).all()
        sql_session.commit()
        results = sorted(results, key=itemgetter(1))
        if len(tokens) >= 3 and tokens[2].isdigit() and int(tokens[2]) <= 15:
            amount = int(tokens[2])
        else:
            amount = 3
        if len(tokens) >= 2:
            if tokens[1] == 'top':
                return ("Karma top %s -> %s" %
                        (amount, ", ".join([":".join([str(y) for y in x]) for x in results[-amount:]])), None)
            elif tokens[1] == 'bottom':
                return ("Karma bottom %s -> %s" %
                        (amount, ", ".join([":".join([str(y) for y in x]) for x in results[:amount]])), None)
            elif tokens[1] == 'middle':
                mid_point = int(len(results) / 2)
                return ("Karma middle %s -> %s" %
                        (amount, ", ".join([":".join([str(y) for y in x]) for x in results[mid_point - int(amount / 2 + 1):mid_point + int(amount / 2 + 1)]])), None)
        return ("Highest score: %s (%s) - Lowest score: %s (%s)" % (results[-1][0], results[-1][1], results[0][0], results[0][1]), None)
    else:
        things = sql_session.query(Karma).filter_by(string=token)
        sql_session.commit()
        score = calckarma(things)
        if score:
            return ("'%s' has a score of: %s" % (arguments, score), None)
        else:
            return ("'%s' has neutral karma." % (arguments), None)
