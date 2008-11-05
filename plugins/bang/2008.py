#!/usr/bin/env python
import math
import urllib
import re

def bang(pipein, arguments, event):
	radius = 5
	total = 538.0
	
	red = chr(27) + '[31m'
	blue = chr(27) + '[34m'
	red = chr(3) + '4'
	blue = chr(3) + '12'
	
	cnn = urllib.urlopen("http://www.cnn.com/")
	for each in cnn:
		if each.find('evotes') != -1:
			cand = re.search('"candidates":\[(.*?)\]',each)
			if cand:
				false = False
				true = True
				candict = eval(cand.group(1))
	cand_s = []
	for each in candict:
		cand_s.append('%s has %swon with %s votes and %s electoral votes.' % (each['lname'], not each['winner'] and 'not ' or '', each['cvotes'], each['evotes']))
		if each['party'] == 'D':
			d = each['evotes']
		elif each['party'] == 'R':
			r = each['evotes']	

	piechart = ''
	for y in range(-radius, radius):
		line = ''
		for x in range(-2 * radius, 2 * radius):
			if x < 0 and math.atan((y)/(x/2 + 0.00000001)) * 180 / math.pi + 90 < 320 * d / total:
				color = blue + 'D'
			elif x >= 0 and math.atan((y)/(x/2 + 0.00000001)) * 180 / math.pi + 90 < 320 * (d - 270) / total:
				color = blue + 'D'
			elif x >= 0 and math.atan((-y)/(x/2 + 0.00000001)) * 180 / math.pi + 90 < 360 * r / total:
				color = red + 'R'
			elif x < 0 and math.atan((-y)/(x/2 + 0.00000001)) * 180 / math.pi + 90 < 360 * (r - 270) / total:
				color = red + 'R'
			else:
				color = ' '
			if (x/2)**2 + y**2 < radius ** 2:
				line += color
			else:
				line += ' '
		piechart += line
	if '-pie' in arguments:
		return (piechart, None)
	else:
		return (cand_s, None)

