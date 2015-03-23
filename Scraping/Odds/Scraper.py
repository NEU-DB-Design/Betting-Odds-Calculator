# -*- coding: utf-8 -*-
import requests
from BeautifulSoup import BeautifulSoup
import unicodedata

class Scraper():

	url = 'http://sports.bovada.lv/sports-betting/nba-basketball-lines.jsp'
	sqlStr = 'SELECT Name, Location FROM Game'
	sqlString = 'SELECT ID, Name, Location FROM Team'
	qryStr = '''
			SELECT Id
			FROM Game
			WHERE MONTH(DATE) = MONTH('%s') 
			AND DAY(DATE) = DAY('%s') 
			AND YEAR(DATE) = YEAR('%s') 
			AND (
				(
				team1_id = %s
				AND team2_id = %s
			)
			OR (
				team2_id = %s
				AND team1_id = %s
			)
			)
			LIMIT 1'''
			
	def __init__(self):
		self.LoadCaches()
	
	def Run(self):
		r = requests.get(self.url)
		soup = BeautifulSoup(r.text)

		all = []
		lst = None
		dt = None
		
		scheduleContainer = soup.find('div', id='event-schedule')
		
		for dv in scheduleContainer.findAll('div', recursive=False):
			nm, cnt = dv.attrs[0]
			if cnt == u'schedule-date':
				dt = '------------------DATE--------------'
				if not lst: # If the list is null, this is the first date and we haven't found any odds yet.
					lst = []
				else: # If not save the date and game odds.
					print 'h2'
					all.append((dt, lst))
			else: # Parse individual odds data sections here.
				lst.append(dv)
		if not not lst:
			all.append((dt, lst))
			print 'h2 2nd'
			print dt
			print '----------\n' + str(lst)
		#print all[0]
		return 

		divs = soup.findAll('div', 'event left even')
		divs += soup.findAll('div', 'event left odd')

		betting_lines = []
		for i, div in enumerate(divs):
			print '\nSection: ' + str(i)
			betting_lines.append(self.ParseSection(div))
			
		print '\nCount:'
		print len(divs)
		
	def ParseSection(self, section):
		# Find spreads
		spreads = section.findAll('a', 'lineOdd')
		if not spreads:
			try:
				spreads = section.find('div', 'line-normal').find('span', 'disabled')
			except Exception, e: #If no line-normal found then this bet is 'suspended'
				print 'Parse Error: ' + str(e)
				return
		if not spreads or len(spreads) < 2:
			print 'SPREADS NOT FOUND'
			return None
		else:
			print 'spread 1: ' + spreads[0].text
			print 'spread 1: ' + spreads[1].text
		
		# Find names
		names = section.findAll('a', 'competitor left')
		if not names:
			names = section.findAll('span', 'left disabled')
		if not names or len(names) < 2:
			print 'NAMES NOT FOUND.'
			return None
		#else:
		print 'Team 1: ' + names[0].text
		print 'Team 2: ' + names[1].text
		t1 = names[0].text
		t2 = names[1].text
		
		t1_id = self.CheckTeam(t1)
		t2_id = self.CheckTeam(t2)
		
		if not t1_id or not t2_id:
			return None
			
		date = ''
			
		# Search for the correct game here
		game = self.SearchGame(t1_id, t2_id, date)
			
	def LoadCaches(self):
		self.team_ID_Cache = {}
		#cnx, cursor = self.GetCursor()
		#cursor.execute(self.sqlString)
		#for _id, name, location in cursor.fetchall():
			#key = location.lower() + ' ' + name.lower()
			#if not key in self.team_ID_Cache:
				#self.team_ID_Cache[key] = _id
		print 'cache loaded.'
		
	def SearchGame(self, id1, id2, date):
		#cursor = self.GetCursor()
		#cursor.execute(self.qryStr, (date, date, date, id1, id2, id1, id2))
		return cursor.fetchone()[0]
		
	
	def CheckTeam(self, team):
		t = team.encode('utf8').lower()
		if t.lower() in self.team_ID_Cache:
			return self.team_ID_Cache[t.lower()]
		else:
			return None
		
	def GetCursor(self):
		cnx = MySQLdb.connect(host='', port=3306, passwd='gamera@1234',
					user='bets', db='bets')
		return cnx, cnx.cursor()
		
	def Dump(self, text, location):
		open(location, 'w').write(str(text))
		
sraper = Scraper()
sraper.Run()