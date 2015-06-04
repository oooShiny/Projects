from xml.dom.minidom import parseString
import json

with open('mlb.json') as data_file:    
	data = json.load(data_file)

def find_values(id, json_repr):
	results = []	
	def _decode_dict(a_dict):
		try: results.append(a_dict[id])
		except KeyError: pass
		return a_dict
	json.loads(json_repr, object_hook=_decode_dict) #return value ignored
	return results

class eventdata:
	def __init__(self, teaminfo, gameinfo):
			self.teaminfo = teaminfo
			self.gameinfo = gameinfo
			self.hometeam = find_values('name', json.dumps(self.teaminfo[0]))[0]
			self.awayteam = find_values('name', json.dumps(self.teaminfo[1]))[0]
			self.homescore = find_values('score', json.dumps(self.teaminfo[0]))[0]
			self.awayscore = find_values('score', json.dumps(self.teaminfo[1]))[0]
			self.homelocation = find_values('location', json.dumps(self.teaminfo[0]))[0]
			self.awaylocation = find_values('location', json.dumps(self.teaminfo[1]))[0]
			self.homeabb = find_values('abbreviation', json.dumps(self.teaminfo[0]))[0]
			self.awayabb = find_values('abbreviation', json.dumps(self.teaminfo[1]))[0]
			self.homescore = find_values('score', json.dumps(self.teaminfo[0]))[0]
			self.awayscore = find_values('score', json.dumps(self.teaminfo[1]))[0]
			self.gamestatus = find_values('shortDetail', json.dumps(self.gameinfo))[0]

testdata = []
events = []
	
for i in find_values('events', json.dumps(data)):
	try: i.keys()[0]
	except: events.append(i)
	
for i, j in zip(find_values('competitors', json.dumps(events)), find_values('competitions', json.dumps(events))):
	testdata.append(eventdata(i,j))
#		for info in games:
#			print "The %s are %s with a record of %s wins and %s losses." % (find_values('name', json.dumps(info))[0], find_values('homeAway', json.dumps(info))[0], find_values('wins', json.dumps(info))[0], find_values('losses', json.dumps(info))[0])
#		print "-----------"
#		print games #make it into attribute
		#print "Home: %s, Away: %s, Home Pitcher: %s, Away Pitcher: %s" % (find_values('home'))

for i in testdata:
	if int(i.homescore) > int(i.awayscore):
		print "%s %s (%s) won against %s %s (%s) %s-%s" % (i.homelocation, i.hometeam, i.homeabb, i.awaylocation, i.awayteam, i.awayabb, i.homescore, i.awayscore)
	elif int(i.homescore) < int(i.awayscore):
		print "%s %s (%s) lost against %s %s (%s) %s-%s" % (i.homelocation, i.hometeam, i.homeabb, i.awaylocation, i.awayteam, i.awayabb, i.homescore, i.awayscore)
	else:
		print "%s %s (%s) tied with %s %s (%s) %s-%s" % (i.homelocation, i.hometeam, i.homeabb, i.awaylocation, i.awayteam, i.awayabb, i.homescore, i.awayscore)
	print i.gamestatus
	print "\n"

#print find_values('events', json.dumps(data))