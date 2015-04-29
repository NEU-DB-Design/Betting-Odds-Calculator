'''

Copyright (c) <2015> <Hunt Graham, Mike Kozicky, Daniel Solomon>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.


'''


import requests
import json
import DB
import Cache
from datetime import datetime
import dateutil.parser
import logging
import time

LOG_FILENAME = 'MLB_Schedule.txt'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)


url = 'https://erikberg.com/mlb/results/%s.json'
headers = {'Authorization': 'Bearer afe75781-fd12-4a0a-ac3e-7c60abe05199',
	   'User-agent': 'hunt.b.graham@gmail.com'}

class MLB_Schedule():

	con, cursor = DB.GetCursor(local=True)
	teamCache = Cache.MLB_NameCache(con)
	gameCache = Cache.MLB_GameCache(con)
	dbg = ''
	
	def Run(self):
		for t in reversed(self.GetTeams()):
			#import pdb; pdb.set_trace()
			self.ReadTeam(t)
			self.gameCache.Reload()
			time.sleep(5)

	def ReadTeam(self, team):

		print 'TEAM: ' + team

		# Make API request
		r = requests.get(url % team, headers=headers)
		open('json_dump.txt', 'a').write(r.text)

		# Attempt to parse JSON
		try:
			decoded = json.loads(r.text)
		except:
			#print 'JSON error.'
			return
		#print 'JSON parsed succesfully.'
	
		# Iterate through each game entry in JSON
		for d in decoded:

			# Parse JSON fields for 1st team, 2nd team, date, and 
			# game status
			t1 = d['team']['last_name']
			t2 = d['opponent']['last_name']
			full = d['event_start_date_time']
			completed = d['event_status']
			logging.debug(t1 + '\n' +t2 + '\n')
			#print t1
			#print t2

			t1_score, t2_score = None, None
			if completed == 'completed':
				t1_score = d['team_points_scored']
				t2_score = d['opponent_points_scored']
				#print t1_score
				#print t2_score
				logging.debug(str(t1_score) + '\n' +str(t2_score) + '\n')

			#print '\n'

			# Init new MLB game object.
			game = MLB_Game(t1, t2, full, completed)

			# Validate/Populate team ID fields
			if not game.ValidateTeams(self.teamCache):
				print 'Team cache miss'
				continue
			
			# Check what we have for this game.
			status = game.CheckStatus(self.gameCache)

			# Depending on status, add rows to MLB_Schedule
			# and/or MLB_Outcome
			if status == 1: 
				#print 'Have both!'
				logging.debug('NOTHING')
				continue
			elif status == -1:
				#print 'Schedule'
				self.Add_Schedule(game)
				logging.debug('Adding schedule')
			elif status == 0 and completed == 'completed':  
				#print 'Result'
				self.Add_Result(game, t1_score, t2_score)
				logging.debug('ADDING RESULT!')
			else:
				continue
				#print 'Nothing!'

	def GetTeams(self):
		sql = 'SELECT Location, Name FROM MLB_Team'
		con, cursor = DB.GetCursor(local=True)
		cursor.execute(sql)

		formatFunc = lambda L, n: (L + ' ' + n).replace(' ', '-').replace('.', '').lower()
		return [formatFunc(loc, name) for loc, name in cursor.fetchall()]
		#return [(loc + ' ' + name).replace(' ', '-').replace('.', '') for loc, name in cursor.fetchall()]
		
			


	def Add_Schedule(self, game):
		sql = 'INSERT INTO `bets`.`MLB_Schedule`(`API_GameID`,`Team1_ID`,`Team2_ID`,`Date`,`Result_ID`) VALUES (\'abc123\', %s, %s, %s, %s);'
		con, cursor = DB.GetCursor(local=True)
		cursor.execute(sql, (game.t1_id, game.t2_id, game.Date, None))
		con.commit()
		#print 'Just schedule!'

	def Add_Both(self, sched):
		#print 'Both!'
		pass

	def Add_Result(self, game, score1, score2):
		sql = 'INSERT INTO MLB_Outcome (GameID, Score1, Score2) VALUES (%s, %s, %s);'
		con, cursor = DB.GetCursor(local=True)
		cursor.execute(sql, (game.gameID, score1, score2))
		con.commit()
		#print 'Add Result!'
		#updateSql = 


class MLB_Game():

	Team1 = ''
	Team2 = ''
	Date = None
	IsComplete = False
	t1_id = None
	t2_id = None
	
	def __init__(self, t1, t2, d, ic):
		self.Team1 = t1
		self.Team2 = t2
		self.IsComplete = ic
		date = self._ParseDate(d)
		if date == None:
			logging.debug('FAIL!')
			return None
		self.Date = date

	def ValidateTeams(self, teamCache):
		if self.Team1 in teamCache and self.Team1 in teamCache:
			self.t1_id = teamCache[self.Team1]
			self.t2_id = teamCache[self.Team2]
			return True
		else:
			return False

	##
	## Returns:
	## -1 -> No game or outcome
	##  0 -> No outcome
	##  1 -> Has both
	##
	def CheckStatus(self, gameCache):
		
		k1 = ' '.join([str(i) for i in [self.Date, self.t1_id, self.t2_id]])
		k2 = ' '.join([str(i) for i in [self.Date, self.t2_id, self.t1_id]])
		need_to_switch, has_outcome = False, None

		if k1 in gameCache:
			self.gameID, need_to_switch, has_outcome = gameCache[k1]
		elif k2 in gameCache:
			self.gameID, need_to_switch, has_outcome = gameCache[k2]
			self._SwitchTeams()
		else:
			return -1

		if has_outcome == None:
			#import pdb; pdb.set_trace()
			return 0
		else:
			return 1

	def _SwitchTeams(self):
		self.t1_id, self.t2_id = self.t2_id, self.t1_id 

	def _ParseDate(self, date):
		try:
			d = dateutil.parser.parse(date)		
			return d.strftime('%Y-%m-%d %H:%M:%S')
		except Exception, e:
			#print 'Date parse error: ' + str(e)
			return None


	

ms = MLB_Schedule()
#ms.Run()
#for t in ms.GetTeams():
#	print t
#ms.ReadTeam('chicago-cubs')
#ms.ReadTeam('cincinnati-reds')
#print ms.GetTeams()
'''
ms.ReadTeam('arizona-diamondbacks')
ms.ReadTeam('atlanta-braves')
ms.ReadTeam('baltimore-orioles')
ms.ReadTeam('boston-red-sox')
ms.ReadTeam('chicago-cubs')
ms.ReadTeam('chicago-white-sox')
ms.ReadTeam('cincinnati-reds')
ms.ReadTeam('cleveland-indians')
time.sleep(1)
ms.ReadTeam('colorado-rockies')
time.sleep(1)
ms.ReadTeam('detroit-tigers')
time.sleep(1)
ms.ReadTeam('houston-astros')
time.sleep(1)
ms.ReadTeam('kansas-city-royals')
time.sleep(1)
ms.ReadTeam('los-angeles-angels')
time.sleep(1)
'''
ms.ReadTeam('los-angeles-dodgers')
time.sleep(1)
ms.ReadTeam('miami-marlins')
time.sleep(1)
ms.ReadTeam('milwaukee-brewers')
time.sleep(1)
ms.ReadTeam('minnesota-twins')
time.sleep(1)
ms.ReadTeam('new-york-mets')
time.sleep(1)
ms.ReadTeam('new-york-yankees')
time.sleep(1)
ms.ReadTeam('oakland-athletics')
time.sleep(1)
ms.ReadTeam('philadelphia-phillies')
time.sleep(1)
ms.ReadTeam('pittsburgh-pirates')
time.sleep(1)
ms.ReadTeam('san-diego-padres')
time.sleep(1)
ms.ReadTeam('san-francisco-giants')
time.sleep(1)
ms.ReadTeam('seattle-mariners')
time.sleep(1)
ms.ReadTeam('st-louis-cardinals')
time.sleep(1)
ms.ReadTeam('tampa-bay-rays')
time.sleep(1)
ms.ReadTeam('texas-rangers')
time.sleep(1)
ms.ReadTeam('toronto-blue-jays')
time.sleep(1)
ms.ReadTeam('washington-nationals')
