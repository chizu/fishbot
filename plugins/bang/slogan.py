#!/usr/bin/python
import fishapi,re,urllib

def bang(pipein, arguments, event):
    subject = pipein or arguments
    url = "http://www.sloganizer.net/en/ajax.php"
    data = urllib.urlencode({"slogan":subject, "id":"1326238012-b2cea363a282c4517bdef74a98a964da"})
    f = urllib.urlopen(url, data)
    slogan = f.read().split('<')[1].split('>')[1]
    return (slogan, None)
