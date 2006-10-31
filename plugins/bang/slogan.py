#!/usr/bin/python
import fishapi,re

def bang(pipein, arguments, event):
    subject = pipein or arguments
    url = "http://www.sloganizer.net/en/?slogan=%s" + subject
    groups = fishapi.http_grep(url, '<p class="slogan">.<b>(.*)</b>.</p>')
    return (groups[0], None)
