import json
from datetime import datetime
from itertools import groupby

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
		self.gamestatus = status(find_values('shortDetail', json.dumps(self.gameinfo))[0])
		self.gamedate = getdate(self.gamestatus)

def importjson():
	"""Imports json file to python"""
	with open('mlb.json') as data_file:    
		data = json.load(data_file)
	return data

def find_values(id, json_data):
	"""Finds values of specific keywords in json file"""
	results = []	
	def _decode_dict(a_dict):
		try:
			results.append(a_dict[id])
		except KeyError: 
			pass
		return a_dict
	json.loads(json_data, object_hook=_decode_dict) #return value ignored
	return results

def status(status):
	"""Evaluates game status and converts date/time if needed"""
	if 'o' in status:
		return status
	elif status == "Final":
		return status
	else:
		d = datetime.strptime("%s" % status, "%Y-%m-%dT%H:%M:%SZ")
		return d

def getdate(status):
	if type(status) is datetime:
		d = status.strftime("%B %-d, %Y")
		return d
	elif "o" in status:
		return "Live"
	else:
		return ""
		
def grabevents(data):
	"""Organizes games into class"""
	events = []
	finaldata = []
	for i in find_values('events', json.dumps(data)):
		try: i.keys()[0]
		except: events.append(i)
	for i, j in zip(find_values('competitors', json.dumps(events)), find_values('competitions', json.dumps(events))):
		finaldata.append(eventdata(i,j))
	return finaldata

def htmlconvert(finaldata):
	"""Converts data to HTML"""
	htmldata = []
	for i in finaldata:
		if type(i.gamestatus) is datetime:
			htmldata.append("<td><table><tr><td><table><tr><td>%s</td><td>%s</td></tr><tr><td width=100px;>%s</td><td>%s</td></tr></table></td><td width=108px;>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%s<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%s</td></tr></table></td>" % (i.hometeam, i.homescore, i.awayteam, i.awayscore, i.gamedate, i.gamestatus.strftime("%I:%M %p")))
		else: 
			htmldata.append("<td><table><tr><td><table><tr><td>%s</td><td>%s</td></tr><tr><td width=100px;>%s</td><td>%s</td></tr></table></td><td width=108px;>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%s<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%s</td></tr></table></td>" % (i.hometeam, i.homescore, i.awayteam, i.awayscore, i.gamedate, i.gamestatus))

	for place in range(len(htmldata)):
		if place % 2 == 0:
			htmldata[place] = "<tr>%s" % (htmldata[place])
		else:
			htmldata[place] = "%s</tr>" % (htmldata[place])
	
	return htmldata
	
def main():
	data = importjson()
	finaldata = grabevents(data)
	htmldata = htmlconvert(finaldata)
	htmlfinal =["<html><body><table border='1'>"]
	for i in htmldata:
		htmlfinal.append(i)
	htmlfinal.append("</table></body></html>")
	
	handle=open("mlb.html",'w+')
	handle.write("".join(htmlfinal))
	handle.close();
if  __name__ =='__main__':main()