#!/usr/bin/python
"""!weather - Weather lookup"""
import urllib, re, fishapi

def bang(pipein, arguments, event):
    location = pipein or arguments
    url = "http://rss.wunderground.com/auto/rss_full/%s.xml?units=both" % location
    groups = fishapi.http_grep(url, "<title>(.*?) Weather from Weather Underground</title>.*?<\!\[CDATA\[(.*?)\]\]>")
    return (groups[0] + ' - ' + groups[1], None)
