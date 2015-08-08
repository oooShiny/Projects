import urllib2
from bs4 import BeautifulSoup
import os

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
champs=[]

class champions:
	def __init__(self, code):
		self.code = code
		self.name = code.span.text
		self.jsonname = self.name.replace(' ', ''). replace('.', '').replace("'", '')
		self.positions = code.findAll('a', {"style" : "display:block"})
		self.lanes = get_lanes(self.positions, self.name)
		self.json = create_json(self.lanes, self.jsonname)

def find_champ():
	url = "http://champion.gg"
	ourUrl = opener.open(url).read()
	soup = BeautifulSoup(ourUrl)
	soup.prettify()
	for i in soup.findAll('div', {"class" : "champ-index-img"}):
		champs.append(champions(i))

def get_lanes(lane, name):
	dic = {}
	url = "http://champion.gg"
	ourUrl = opener.open(url).read()
	soup = BeautifulSoup(ourUrl)
	soup.prettify()
	for i in lane:
		print "Getting build for %s %s" % (i.text.strip(), name)
		dic.update({"%s %s" % (i.text.strip(), soup.find('div', {"class" : "analysis-holder"}).small.strong.text):{"Most Frequent Core Build":get_items(i['href'], 0), "Highest Win % Core Build":get_items(i['href'], 1), "Most Frequent Starters":get_items(i['href'], 2), "Highest Win % Starters":get_items(i['href'], 3)}})
	return dic

def get_items(url, which):
	url = "http://champion.gg%s" % url
	ourUrl = opener.open(url).read()
	soup = BeautifulSoup(ourUrl)
	soup.prettify()	
	items=[]
	for pos, i in enumerate(soup.findAll('div', {"class" : "build-wrapper"})):
		if pos == which:
			for j in i.findAll('img'):
				if j['src'].replace('.png', '')[-4:] == "2010":
					items.append('{"count": 1, "id": "2003"}')
				else:
					items.append('{"count": 1, "id": "%s"}' % j['src'].replace('.png', '')[-4:])
	return items

def create_json(lanes, name):
	for pos,i in enumerate(lanes):
		d = lanes[i]
		template = '{"map": "any", "isGlobalForChampions": false, "blocks": [{"items": [%s], "type": "Most Frequent Starters"}, {"items": [%s], "type": "Highest Win Rate Starters"}, {"items": [%s], "type": "Most Frequent Build"}, {"items": [%s], "type": "Highest Win Rate Build"}, {"items":[{"count":1,"id":"3340"},{"count":1,"id":"3341"},{"count":1,"id":"3342"},{"count":1,"id":"2044"},{"count":1,"id":"2043"}],"type":"Trinkets and Wards"}], "associatedChampions": [], "title": "%s", "priority": false, "mode": "any", "isGlobalForMaps": true, "associatedMaps": [], "type": "custom", "sortrank": 1, "champion": "%s"}' % (','.join(map(str,d[d.keys()[2]])), ','.join(map(str,d[d.keys()[3]])), ','.join(map(str,d[d.keys()[1]])), ','.join(map(str,d[d.keys()[0]])), i, name)
		create_file(template, name, i)	

def create_file(json, name, lane):
	directory = "Champions/%s/Recommended" % (name)
	filename = '%s.json' % lane.replace('.', '_').replace(' ', '_')
	if not os.path.exists(directory):
		os.makedirs(directory)
	with open(os.path.join(directory, filename), 'wb') as temp_file:
		temp_file.write(json)
	
def main():
	find_champ()
		
if  __name__ =='__main__':main()
