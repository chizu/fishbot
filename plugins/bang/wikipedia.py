#!/usr/bin/python
"""Fishbot Wikipedia Lookup"""
import urllib,re

# Spoof Firefox for the purposes of querying
#urllib.URLopener.version = """Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.8) Gecko/20050609 Firefox/1.0.4"""

def handle_say(self, source, to, message):
    # self here is going to be the main Fishbot object
    respond = self.respond_to(source, to)

    if (re.search("^!wikipedia (.*)", message)):
	# probably shouldn't be considered a simple command.
	# maybe break this off into another function
	google = re.search("^!wikipedia (.*)",message)
	# generate search URL
	search_page = urllib.urlopen("http://www.google.com/search?hl=en&q="+ re.sub(" ", "+", google.group(1)) +"+site:en.wikipedia.org&btnG=Google+Search")
	search_page = search_page.readlines()
	for each in search_page:
	    # wade through googles mass of html to pull out the first title
	    # and url.
	    if re.compile("<\!--m-->(.*?)<\/a>", re.M).search(each):
		try:
		    self.say(respond, "Wikipedia - '" + google.group(1) + "'| " + re.sub("<.*?>","",re.compile("<\!--m-->(.*?)<\/a>", re.M).search(each).group(1)) + " [ " + re.search("<\!--m-->.*?<a.*?href=\"(.*?)\">", each, re.M).group(1) + " ]")
		    return
		except:
		    self.say(respond, "Look it up yourself, Google sucks.")
		    return
