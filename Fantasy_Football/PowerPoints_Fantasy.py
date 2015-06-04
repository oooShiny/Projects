#!/usr/bin/python
import urllib2
from BeautifulSoup import BeautifulSoup
import re
import sys
import operator
from collections import OrderedDict

league = input("Enter League ID: ")
week = input("Enter Week: ")

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

scoreA=[]
scoreB=[]
score1=OrderedDict({})
score2=OrderedDict({})
AllTeams = []

class TeamID:
	def __init__(self, name, ID, w, wins, losses, pr, bool):
			self.name = name
			self.ID = ID
			self.w = w
			self.wins = wins
			self.losses = losses
			self.pr = pr
			self.bool = bool
	
def gather_teams():
	"""Gathers team names and ID numbers in the specified league"""
	url = "http://games.espn.go.com/ffl/standings?leagueId=%s&seasonId=2014" % (league)
	ourUrl = opener.open(url).read()
	soup = BeautifulSoup(ourUrl)
	for i in soup.findAll('tr', {'class' : 'tableBody'}):
		AllTeams.append(TeamID('%s' % (i.find('a').text), '%s' % (i.find('a')['href'].replace('/ffl/clubhouse?leagueId=%s&teamId=' % league,'').replace('&seasonId=2014','')), [], '0', '0', '', True))
	for i in AllTeams:
		i.ID = int(i.ID)
		print "%s found with team ID %s" % (i.name.replace('  ', ' '), i.ID)

def gather_matchups(w):
	"""Determines which team is playing which in the defined week"""
	url = "http://games.espn.go.com/ffl/scoreboard?leagueId=%s&scoringPeriodId=%s" % (league, w)
	ourUrl = opener.open(url).read()
	soup = BeautifulSoup(ourUrl)
	matchups = [item.text for item in soup.findAll("div", { "class" : "name" })]
	for x,i in enumerate(matchups):
		matchups[x] = i.replace(i, i.split('(')[0])
	return matchups

def scores(teamA, teamB, w):
	"""Determines the score for each team in the defined week"""
	for a,b in zip(teamA,teamB):
		for i in AllTeams:
			if a == i.name:
				url = "http://games.espn.go.com/ffl/boxscorequick?leagueId=%s&teamId=%s&scoringPeriodId=%s&seasonId=2014&view=scoringperiod&version=quick" % (league, i.ID, w)
				ourUrl = opener.open(url).read()
				soup = BeautifulSoup(ourUrl)
				match = [item.text for item in soup.findAll("div", { "class" : "danglerBox totalScore" })]
				i.w.append(float(match[0]))
				scoreA.append(float(match[0]))
				score1[a] = float(match[0])
				print "%s: %s" % (i.name.replace('  ', ' '), match[0])
			if b == i.name:
				url = "http://games.espn.go.com/ffl/boxscorequick?leagueId=%s&teamId=%s&scoringPeriodId=%s&seasonId=2014&view=scoringperiod&version=quick" % (league, i.ID, w)
				ourUrl = opener.open(url).read()
				soup = BeautifulSoup(ourUrl)
				match = [item.text for item in soup.findAll("div", { "class" : "danglerBox totalScore" })]
				i.w.append(float(match[0]))
				scoreB.append(float(match[0]))
				score2[b] = float(match[0])
				print "%s: %s" % (i.name.replace('  ', ' '), match[0])
	
				
def winner(score1, score2):
	"""Determines if each team won or lost in the defined week"""
	for i in AllTeams:
		for j,k in zip(score1,score2):
			if i.name == j:
				if score1[j] == score2[k]:
					print '%s tied against %s (%s-%s)' % (j.replace('  ', ' '),k.replace('  ', ' '),score1[j],score2[k])
				elif score1[j] > score2[k]:
					i.wins = int(i.wins) + 1
					print '%s won against %s (%s-%s)' % (j.replace('  ', ' '),k.replace('  ', ' '),score1[j],score2[k])
				elif score1[j] < score2[k]:
					i.losses = int(i.losses) + 1
					print '%s lost against %s (%s-%s)' % (j.replace('  ', ' '),k.replace('  ', ' '),score1[j],score2[k])
			elif i.name == k:
				if score2[k] == score1[j]:
					print '%s tied against %s (%s-%s)' % (k.replace('  ', ' '),j.replace('  ', ' '),score2[k],score1[j])
				elif score2[k] > score1[j]:
					i.wins = int(i.wins) + 1
					print '%s won against %s (%s-%s)' % (k.replace('  ', ' '),j.replace('  ', ' '),score2[k],score1[j])
				elif score2[k] < score1[j]:
					i.losses = int(i.losses) + 1
					print '%s lost against %s (%s-%s)' % (k.replace('  ', ' '),j.replace('  ', ' '),score2[k],score1[j])
	
def power_points():
	"""Determines each team's power points"""
	for i in AllTeams:
		if (int(i.wins) + int(i.losses)) > 0:
			part1 = sum(i.w)/len(i.w)*6
			part2 = (max(i.w) + min(i.w))*2
			part3 = (float(i.wins)/(float(i.wins)+float(i.losses)))*400
			i.pr = (part1 + part2 + part3)/10
		else:
			i.pr = float(0)
	AllTeams.sort(key=operator.attrgetter('pr'), reverse = True)
			
def main():
	gather_teams()
	i = 1
	while i <= int(week):
		print "\nGathering data for Week %s" % (i)
		print "Gathering Matchups"
		matchups = gather_matchups(str(i))
		teamA = matchups[::2]
		teamB = matchups[1::2]
		print "Matchups found"
		print "Gathering scores"
		print "--------------------"
		scores(teamA,teamB,str(i))
		print "--------------------"
		print "Scores found"
		print "Determining wins and losses"
		print "--------------------"
		winner(score1,score2)
		print "--------------------"
		print "Week %s done\n" % (i)
		score1.clear()
		score2.clear()
		scoreA=[]
		scoreB=[]
		i+=1
	power_points()
	print "WEEK %s POWER RANKINGS" % (week)
	print "----------------------------------"
	for i,j in enumerate(AllTeams):
		print "%s %s %s-%s (%s)" % (i+1, j.name.replace('  ', ' '), j.wins, j.losses, j.pr)



	
if  __name__ =='__main__':main()
