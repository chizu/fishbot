#!/usr/bin/python
"""Fishbot Convert Lookup"""
import urllib,re

# Spoof Firefox for the purposes of googling.
urllib.URLopener.version = """Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.8) Gecko/20050609 Firefox/1.0.4"""

def handle_say(self, source, to, message):
    # self here is going to be the main Fishbot object
    respond = self.respond_to(source, to)

    if (re.search("^!convert (.*)", message)):
	# probably shouldn't be considered a simple command.
	# maybe break this off into another function
	google = re.compile("^!convert (.*)").search(message)
	# generate search URL
	search_page = urllib.urlopen("http://www.google.com/search?hl=en&q="+ re.sub(" ", "+", google.group(1)) +"&btnG=Google+Search")
	search_page = search_page.readlines()
	for each in search_page:
	    # wade through googles mass of html to pull out the conversion
	    if re.compile("<font size\=\+1><b>(.*?)<\/b>", re.M).search(each):
		try:
		    response = re.compile("<font size\=\+1><b>(.*?)<\/b>", re.M).search(each).group(1)
		    response = re.sub('<sup>', '^', response)
		    response = re.sub('<.*?>', '', response)
		    response = re.sub('([0-9]) ([0-9])', '\\1,\\2', response)
		    entities = re.findall('\&#(.*?)\;', response)
		    for n in entities:
			response = re.sub('&#'+n+';', chr(int(n)), response)
		    self.say(respond, "Conversion | " + response )
		    return
		except NameError:
		    self.say(respond, "Look it up yourself, Google sucks.")
		    return
