#!/usr/bin/python
import urllib,string,re

def bang(pipein, arguments, event):
    subject = pipein or arguments
    url = "http://www.sloganizer.net/en/?slogan=%s" + re.sub(" ", "+", subject)
    groups = fishapi.http_grep(url, '<p class="slogan">.<b>(.*)</b>.</p>')
    return (groups[0], None)
