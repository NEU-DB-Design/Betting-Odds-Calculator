import requests
import urllib2
import json
import xml.etree.ElementTree as ET
from lxml import objectify
import MySQLdb


class ScheduleScraper():

	'''
	SELECT * 
		FROM  `Team` 
		WHERE CONCAT( Location,  ' ', Name ) =  'Boston Celtics'
	'''
	
	sqlString = 'SELECT ID, Name, Location FROM Team'
	instStr = 'INSERT INTO Game (team1_id, team2_id, date) VALUES (%s, %s, %s);'
	url = 'http://api.sportsdatallc.org/nba-t3/games/2014/REG/schedule.json?api_key=3m8xndzddcvjc9wahux5wvye'

	def __init__(self):
		self.LoadCaches()
	
	##
	## Initialize team ID cache
	##
	def LoadCaches(self):
		self.teamCache = {}
		cnx, cursor = self.GetCursor()
		cursor.execute(self.sqlString)
		for _id, name, location in cursor.fetchall():
			key = location.lower() + ' ' + name.lower()
			if not key in self.teamCache:
				self.teamCache[key] = _id
		print 'cache loaded.'
	
	def Run(self):
		r = requests.get(self.url)
		decoded = json.loads(r.text)
		self.Dump(json.dumps(decoded, indent=4, sort_keys=True))
		

		for game1 in decoded['games']:
			# home team
			homename = game1['home']['name']
			home_id = self.CheckTeam(homename)

			# away team
			awayname = game1['away']['name']
			away_id = self.CheckTeam(awayname)
			
			if not home_id or not away_id:
				print 'Invalid team'
				continue

			date = game1['scheduled']
			
			if not date:
				continue
			data = (home_id, away_id, date)

			cnx, cursor = self.GetCursor()
			cursor.execute(self.instStr, data)
			cnx.commit()

	def GetCursor(self):
		cnx = MySQLdb.connect(host='', port=3306, passwd='gamera@1234', 
					user='bets', db='bets')
		return cnx, cnx.cursor()

	
	def CheckTeam(self, team):
		t = team.encode('utf8').lower()
		if t.lower() in self.teamCache:
			return self.teamCache[t.lower()]
		else:
			return None

	def Dump(self, txt):
		open('xmldump.txt', 'w').write(txt)
		
sc = ScheduleScraper()
sc.Run()
