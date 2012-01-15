#!/usr/bin/python
"""!s - Regular expression substitution. Options available are:
The python standard re ones, some perl style (i), and a number for
number of lines to scan (0-9).
Usage: !s/<select>/<replace>/<options>"""
import re,sys,os,string,difflib
import fishapi

def bang(pipein, arguments, event):
	# This regexp is to split correctly on only unescaped / slashes like
	# 'asjdf/as[ad/c]df/as\/df' needs.
	# Returns ['asjdf', 'as[ad/c]df', 'as\\/df']
	unescaped_slash = re.compile(r"(?<!\\)(?<!\[)/(?!.?\])")
	if len(unescaped_slash.split(arguments)) == 4:
		# Assumed to start with s/
		(pattern, repl, options) = unescaped_slash.split(arguments)[1:]
		# Number of lines to search
		lines = 20
		# Number of lines to match
		if re.search('([1-9])', options):
			lines_returned = int(re.search('([1-9])', options).group(0)) + 1
		else:
			lines_returned = 1
		# Search globally, or just the user executing the command
		if 'm' in options or 'M' in options or 'g' in options or 'G' in options:
			search_domain = fishapi.backend.last(type(event), event.target, lines)[1:]
		else:
			search_domain = fishapi.backend.last(type(event), event.source, lines)[1:]
		for past_event in search_domain:
			past_event.arguments = past_event.arguments.replace('\001ACTION', fishapi.getnick(past_event.source))
			past_event.arguments = past_event.arguments.replace('\001', '')
		try:
			option_values = {'I':re.I, 'L':re.L, 'M':re.M, 'S':re.S, 'U':re.U, 'X':re.X, 'G':re.M,
							 'i':re.I,			 'm':re.M,                               'g':re.M}
			# eval, be careful changing this as to not allow arbitrary
			# python to be executed
			compiled = re.compile(pattern, options and eval('|'.join(options), None, option_values) or 0)
			returned = []
			for pevent in search_domain:
				if compiled.search(pevent.arguments):
					returned.append("%s meant to say: %s" % (fishapi.getnick(pevent.source), compiled.sub(repl, pevent.arguments).replace("\/", "/")))
			if len(returned) > lines_returned:
				returned = returned[:lines_returned]
			return (returned, None)
		except:
			raise
	else:
		return ("Wrong number of /'s.", None)
