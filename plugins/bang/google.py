#!/usr/bin/python
"""!google - Fishbot google search"""
import re, fishapi

def bang(pipein, arguments, event):
	search = pipein or arguments
	url = "http://www.google.com/search?hl=en&q=" + re.sub(" ", "+", search) + "&btnG=Google+Search"
	groups = fishapi.http_grep(url, """<!--m-->.*?href="(.*?)".*?>(.*?)</a>(.*?)<span""")
	return ("Google - '%s' | %s | %s [ %s ]" % (search, re.sub("<.*?>", "", groups[1]),	re.sub("<.*?>", "", groups[2]), groups[0]), None)
