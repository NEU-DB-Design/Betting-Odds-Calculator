import requests
import MySQLdb
import json
import simplejson 
from time import sleep
from Cache import NicknameCache

'''
	Results Class:
		Adds Results for all games from the previous day.
		1) Queries all games from the previous day that do not have corresponding entries
		   in rows.
		2) For each result_id ID returned (this corresponds specifically to the SportsData API)
		   make a request to SportsData API for this results Game Box score
		3) 
'''
class Results():
	
	url = 'http://api.sportsdatallc.org/nba-t3/games/%s/boxscore.json?api_key=3m8xndzddcvjc9wahux5wvye'

	def __init__(self):
		self.cnx = MySQLdb.connect(host='', port=3306, passwd='gamera@1234', 
					user='bets', db='bets')
		self.cursor = self.cnx.cursor()
		self.nicknameCache = NicknameCache(self.cnx)

	def __del__(self):
		self.cnx.close()
	
	def ResetCursor(self):
		self.cursor.close()
		self.cursor = self.cnx.cursor()

	
	def Update(self):
		
		self.cursor.callproc('getYesterdaysGames')
		games = self.cursor.fetchall()
		for res_id, t1_id, game_id in games:
			print res_id
			self.UpdateGame(res_id, t1_id, game_id)
			sleep(1)
	
	def UpdateGame(self, api_teamid, team1_id, g_id):
		self.ResetCursor()
		reqStr = self.url % api_teamid
		r = requests.get(reqStr)

		try:
			decoded = simplejson.loads(r.text)
		except Exception, e:
			print 'JSON Error:  ' + str(e) + '\n'
			return
		
		score_1 = decoded['home']['points']
		score_2 = decoded['away']['points']
		
		home = decoded['home']['name']
		away = decoded['away']['name']

		print home
		print score_1
		print away
		print score_2
		
		if home in self.nicknameCache:
			print 'cache miss HOME'

		if away in self.nicknameCache:
			print 'cache miss AWAY'
			
		t1_id = home in self.nicknameCache
		t2_id = away in self.nicknameCache

		# Swap score1 & score2 if SportsData API representation is backwards
		if not team1_id == t1_id:
			score_1, score_2 = score_1, score_2

		data = (score_1, score_2, score_1 > score_2, g_id)
		print '\n'

		self.AddResult(data)


	def AddResult(self, data):
		try:
			self.cursor.callproc('addResult', data)
		except Exception, e:
			print 'SQL Error:  ' + str(e)
		self.cnx.commit()
		
r = Results()
r.Update()
