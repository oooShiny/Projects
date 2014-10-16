#!/usr/bin/python
import urllib2
from BeautifulSoup import BeautifulSoup
import re
import sys
import operator
import string
from collections import OrderedDict

class info:
	def __init__(self, favorite, underdog, linetotal, line, total):
		self.favorite = favorite
		self.underdog = underdog
		self.linetotal = linetotal
		self.line = linetotal[::2]
		self.total = linetotal[1::2]

"""Set up website to be parsed"""
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
url = "http://www.footballlocks.com/nfl_lines.shtml"
ourUrl = opener.open(url).read()
soup = BeautifulSoup(ourUrl)

tds = []
date = []
home = []
linetotal = []
line = []
total = []
away = []
matchups = OrderedDict({})
homenumber = []
awaynumber = []
homesemi = []
awaysemi =[]



for i in soup.findAll('p'):
	for j in i.findAll('td'):
		if j:
			tds.append(j)
for i,j in enumerate(tds):
	if " ET" in j.text:
		date.append(j.text)
	if "-" in j.text:
		home.append(tds[i-1].text)
		away.append(tds[i+1].text)
	if re.match("^[0-9.-]+$", j.text):
		linetotal.append(float(j.text))
	

line = linetotal[::2]
total = linetotal[1::2]

for i,j in zip(home, away):
	matchups[i] = j
for i,j in zip(line, total):
	homenumber.append(round(j/2 - i, 0))
	awaynumber.append(round(j/2 + i, 0))
for i,j in zip(home, homenumber):
	homesemi.append("%s (%s) " % (i, j))

for i,j in zip(away, awaynumber):
	awaysemi.append("%s (%s) " % (i, j))

for i,j, in zip(awaysemi, homesemi):
	if "At " in j:
		print i + j
	else:
		print j + i