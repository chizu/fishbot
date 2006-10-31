#!/usr/bin/python
import fishapi,re,urllib

def bang(pipein, arguments, event):
    subject = pipein or arguments
    url = "http://www.sloganizer.net/en/?%s" % urllib.urlencode({'slogan':subject})
    groups = fishapi.http_grep(url, '<p class="slogan">.<b>(.*)</b>.</p>')
    print groups
    return (groups[0], None)
