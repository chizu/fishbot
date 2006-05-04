#!/usr/bin/python
"""!bash - Retreive bash.org quotes.
Usage: !bash"""
import urllib,string,re,xml.dom.minidom,HTMLParser

def handle_say(self, source, to, message):
    respond = self.respond_to(source, to)
    resource = urllib.urlopen("http://bash.org/xml/?random&num=1&above=10")
    xhtml = resource.readlines()
    dom = xml.dom.minidom.parseString(string.join(xhtml))
    text = dom.getElementsByTagName("item")[0].childNodes[5].childNodes[0].data
    #re.sub("",htmlparser.handleentityref("\1"),text)
    text = re.sub("&quot;", "\"", text)
    text = re.sub("&lt;", "<", text)
    text = re.sub("&gt;", ">", text)
    for each in text.split("<br />"):
	self.say(respond, each)
