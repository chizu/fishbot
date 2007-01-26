#!/usr/bin/python
"""!convert - Convert between things using google."""
import urllib,re
import urllib, re, fishapi

def bang(pipein, arguments, event):
    search = pipein + " " + arguments
    search = search.replace("+","%2B")
    url = "http://www.google.com/search?hl=en&q="+ re.sub(" ", "+", search) +"&btnG=Google+Search"
    groups = fishapi.http_grep(url, "<font size\=\+1><b>(.*?)<\/b>")
    try:
        response = re.sub('<sup>', '^', groups[0])
        response = re.sub('<.*?>', '', response)
        response = re.sub('([0-9]) ([0-9])', '\\1,\\2', response)
        entities = re.findall('\&#(.*?)\;', response)
        for n in entities:
            response = re.sub('&#'+n+';', chr(int(n)), response)
        return (response, None)
    except NameError:
        return ("Look it up yourself, Google sucks.", None)
