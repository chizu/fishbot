#!/usr/bin/python
"""!weather - Weather lookup"""
import urllib, re, fishapi

def bang(pipein, arguments, event):
    location = pipein or arguments
    url = "http://rss.wunderground.com/auto/rss_full/%s.xml?units=both" % location
    groups = fishapi.http_grep(url, "<\!\[CDATA\[(.*?)\]\]>")
    return (location + ' - ' + urllib.unquote(groups[0]), None)
