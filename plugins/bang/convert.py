#!/usr/bin/python
"""!convert - Convert between things using google."""
import urllib,re
import urllib, re, fishapi

def bang(pipein, arguments, event):
    search = pipein + " " + arguments
    url = "http://www.google.com/search?hl=en&q="+ re.sub(" ", "+", search) +"&btnG=Google+Search"
    groups = fishapi.http_grep(url, "<font size\=\+1><b>(.*?)<\/b>")
    try:
        response = re.sub('<sup>', '^', groups[1])
        response = re.sub('<.*?>', '', response)
        response = re.sub('([0-9]) ([0-9])', '\\1,\\2', response)
        entities = re.findall('\&#(.*?)\;', response)
        for n in entities:
            response = re.sub('&#'+n+';', chr(int(n)), response)
        return (response, None)
    except NameError:
        return ("Look it up yourself, Google sucks.", None)

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
