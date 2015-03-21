import requests
import urllib2
import json
import xml.etree.ElementTree as ET
from lxml import objectify


class ScheduleScraper():
	'''
	SELECT * 
		FROM  `Team` 
		WHERE CONCAT( Location,  ' ', Name ) =  'Boston Celtics'
	'''

	url = 'http://api.sportsdatallc.org/nba-t3/games/2014/REG/schedule.json?api_key=3m8xndzddcvjc9wahux5wvye'
	
	def Dump(self, txt):
		open('xmldump.txt', 'w').write(txt)
	
	def Run(self):
		r = requests.get(self.url)
		decoded = json.loads(r.text)

		self.Dump(json.dumps(decoded, sort_keys=True, indent=4))
		
		game1 = decoded['games'][0]

		# home team
		homename = game1['home']['name']
		homealias = game1['home']['alias']
		homeid = game1['home']['id']
		
		# away team
		awayname = game1['away']['name']
		awayalias = game1['home']['alias']
		awayid = game1['home']['id']
		
		id = game1['id']
		venue = game1['venue']['city'] + ' ' + game1['venue']['name']
		date = game1['scheduled']
		
		
		print id
		print venue
		
		print homename
		print awayalias
		print awayid
		
		print awayname
		return True
		
sc = ScheduleScraper()
sc.Run()