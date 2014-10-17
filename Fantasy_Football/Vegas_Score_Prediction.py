#!/usr/bin/python
import urllib2
from BeautifulSoup import BeautifulSoup
import re
import sys
import operator
import string
from collections import OrderedDict

class info:
	def __init__(self, favorite, underdog, linetotal, line, total, matchups, favpoints, undpoints, finalfav, finalund):
		self.favorite = favorite
		self.underdog = underdog
		self.linetotal = linetotal
		self.line = line
		self.total = total
		self.matchups = matchups
		self.favpoints = favpoints
		self.undpoints = undpoints
		self.finalfav = finalfav
		self.finalund = finalund

info = info([],[],[],[],[],OrderedDict({}),[],[],[],[])

def gather():
	"""Set up website to be parsed"""
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	url = "http://www.footballlocks.com/nfl_lines.shtml"
	ourUrl = opener.open(url).read()
	soup = BeautifulSoup(ourUrl)	
	
	"""Parse website"""
	tds = []
	for i in soup.findAll('p'):
		for j in i.findAll('td'):
			if j:
				tds.append(j)
	
	"""Put information in class"""
	for i,j in enumerate(tds):
		if "-" in j.text:
			info.favorite.append(tds[i-1].text)
			info.underdog.append(tds[i+1].text)
		if re.match("^[0-9.-]+$", j.text):
			info.linetotal.append(float(j.text))
	info.line = info.linetotal[::2]
	info.total = info.linetotal[1::2]

def modify():
	"""Modify data for output"""
	for i,j in zip(info.favorite, info.underdog):
		info.matchups[i] = j
	for i,j in zip(info.line, info.total):
		info.favpoints.append(round(j/2 - i, 0))
		info.undpoints.append(round(j/2 + i, 0))
	for i,j in zip(info.favorite, info.favpoints):
		info.finalfav.append("%s (%s) " % (i, j))
	for i,j in zip(info.underdog, info.undpoints):
		info.finalund.append("%s (%s) " % (i, j))

def final():
	"""Print final data"""
	for i,j, in zip(info.finalund, info.finalfav):
		if "At " in j:
			print i + j
		else:
			print j + i

def main():
	gather()
	modify()
	print "Vegas Score Predictions\n"
	final()

if  __name__ =='__main__':main()