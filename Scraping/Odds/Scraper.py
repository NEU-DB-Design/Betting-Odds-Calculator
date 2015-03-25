# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import unicodedata
import MySQLdb
import string
import datetime 
from Models import BettingLine, Date

class Scraper():

	url = 'http://sports.bovada.lv/sports-betting/nba-basketball-lines.jsp'
	sqlStr = 'SELECT Name, Location FROM Game'
	sqlString = 'SELECT ID, Name, Location FROM Team'
	# TODO may be easier to just load a dictionary of games for today/tomorrow
	str1 = '''
		SELECT id, team1_id, team2_id, DATE(date) FROM `Game` 
		WHERE 
			DATE(date) = DATE(NOW()) OR DATE(date) = DATE_ADD(DATE(NOW()), INTERVAL 1 DAY);

		'''
	newstr = '''
			SELECT id, team1_id, team2_id, date 
			FROM Game
			WHERE MONTH(DATE) = %s
				AND (DAY(DATE) = %s OR DAY(DATE) = DATE_ADD(%s, INTERVAL 1 DAY))
				AND YEAR(DATE) = %s
			LIMIT 1'''

	qryStr = '''
			SELECT Id
			FROM Game
			WHERE MONTH(DATE) = %s
			AND DAY(DATE) = %s
			AND YEAR(DATE) = %s
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
	months = {
		'January': 1,
		'February': 2,
		'March': 3,
		'April': 4,
		'May': 5,
		'June': 6,
		'July': 7,
		'August': 8,
		'September': 9,
		'October': 10,
		'November': 11,
		'December': 12
		}
			
	def __init__(self):
		self.LoadCaches()
		self.LoadGameCache()
	
	def Run(self):
		r = requests.get(self.url)
		soup = BeautifulSoup(r.text)

		lst = []
		dt = None
		
		scheduleContainer = soup.find('div', id='event-schedule')

		for dv in scheduleContainer.findAll('div', recursive=False):
			cnt = ' '.join(dv.attrs['class'])
			# Set this to the date for all odds read until we find another of these
			if cnt == u'schedule-date':
				dt = self.ParseDate(dv)
			# Save this odd to current date.
			else: 
				# try parsing these sections
				section = None
				if cnt == u'event left even' or cnt == u'event left odd':
					section = self.ParseSection(dv, dt)
				if not not section:
					lst.append(section) # Add to DB here
		print len(lst)
	

	def ParseDate(self, section):
		# Find span with date
		dateText = section.find('span').text

		# Split date into month/day/year and strip commas and whitespace
		lts = dateText.split(' ')
		transTab = string.maketrans(',', ' ')
		f = lambda x: str(x).translate(transTab).strip()
		trm = map(f, lts)

		# Find month #
		month = None
		if trm[1] in self.months:
			month = self.months[trm[1]]

		return datetime.date(year=int(trm[3]), month=month, day=int(trm[2]))
	

	def ParseSpread(self, spread):
		spread = spread.strip()
		spr = None
		
		for i, ch in enumerate(spread):
			if ch == u'½':
				spr = int(spread[0:i])
				if spread[0] == u'-':
					spr -= 0.5
				else:
					spr += 0.5
				break
			elif ch == u'(':
				spr = int(spread[0:i])
				break
		if not spr:
			spr = int(spread)

		return spr

		
	def ParseSection(self, section, date):
		# Find spreads

		#spreads = section.findAll('a', 'lineOdd')
		spreads = section.find('a', 'lineOdd')
		if not spreads:
			#print 'not spreads'
			try:
				#spreads = section.find('div', 'line-normal').find('span', 'disabled')
				spreads = section.find('div', 'line-normal').find('span')
				#print 'SPREAD 1  ' +  spr 
			except Exception, e: #If no line-normal found then this bet is 'suspended'
				print 'Parse Error: ' + str(e)
				return None

		if not spreads :
			return None

		ml1, ml2 = None, None
		try:
			conts = section.findAll('div', 'moneyline-line-normal')
			ml1 = int(conts[0].text)
			ml2 = int(conts[1].text)
		except Exception, e:	
			print 'MoneyLine Error:  ' + str(e)

		if not not ml1 and not not ml2:
			print 'ML 1: ' + str(ml1)
			print 'ML 2: ' + str(ml2)
		

		print 'spread 1: ' + spreads.text
		ps = self.ParseSpread(spreads.text)
		print 'parsed spread: ' + str(ps)

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
			print 'Team not found :('
			return None

		#print 'FOUND!!!!!!'
		game_id = self.FindGame(t1_id, t2_id, date)

		# spread and ML are null fo rnow
		if not game_id:
			return None
		self.SaveLine(game_id, ml1, ml2, ps)

	def SaveLine(self, game_id, m1, m2, spread):
		print 'Attempting save...'
		print 'spread to check: ' + str(spread)
		print m1
		print m2
		print game_id
		if not spread:
			print 'spread is null indeed!!'
		try:
			cnx, cursor = self.GetCursor()
			args = (game_id, m1, m2, spread)
			cursor.callproc('createNewOdd', args=args)
			cnx.commit()
		except Exception, e:
			print 'Save Error:  ' + str(e)
			
	def LoadCaches(self):
		self.team_ID_Cache = {}

		cnx, cursor = self.GetCursor()
		cursor.execute(self.sqlString)

		for _id, name, location in cursor.fetchall():
			key = location.lower() + ' ' + name.lower()
			if not key in self.team_ID_Cache:
				self.team_ID_Cache[key] = _id

		print '\nTeam id cache loaded.\n'

	def LoadGameCache(self):
		# Init cache
		self.gameCache = {}

		# Call proc
		cnx, cursor = self.GetCursor()
		cursor.callproc('GetGameKeys')
		
		# Create a key for each team
		for _id, team1id, team2id, date in cursor.fetchall():
			key = str(team1id) + '_' + str(team2id) + '_' + str(date)
			key2 = str(team2id) + '_' + str(team1id) + '_' + str(date)
			#print 'key to check: ' + key 
			if not key in self.gameCache:
				self.gameCache[key] = _id
			if not key2 in self.gameCache:
				self.gameCache[key2] = _id

	def FindGame(self, id1, id2, date):
		key = str(id1) + '_' + str(id2) + '_' + str(date)
		print 'key to check: ' + key 
		if key in self.gameCache:
			print 'found game!\n'
			return self.gameCache[key]
		else:
			print 'no juice\n'
			return None

	def SearchGame(self, id1, id2, date):
		cnx, cursor = self.GetCursor()
		cursor.execute(self.qryStr, (date.month, date.day, date.year, id1, id2, id1, id2))
		if cursor.rowcount > 0:
			(val,) = cursor.fetchall()[0] # 1 elemetn tuple. Stupid.
			return val
		else:
			return None
		
	
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
#print 'RES:  ' + str(sraper.ParseSpread(u'+10'))
sraper.Run()

