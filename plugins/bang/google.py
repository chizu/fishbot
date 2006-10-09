#!/usr/bin/python
"""!google - Fishbot google search"""
import urllib, re, fishapi

# Spoof Firefox for the purposes of googling.
#urllib.URLopener.version = """Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.8) Gecko/20050609 Firefox/1.0.4"""
def bang(pipein, arguments, event):
    search = pipein or arguments
    url = "http://www.google.com/search?hl=en&q="+ re.sub(" ", "+", search) +"&btnG=Google+Search"
    groups = fishapi.http_grep(url, "<\!--m-->.*?<a.*?href=\"(.*?)\">(.*?)</a>")
    return ("Google - '%s' | %s [ %s ]" % (search, re.sub("<.*?>", "", groups[1]), groups[0]), None)

