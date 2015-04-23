import MySQLdb

class CacheBase():
	
	def __init__(self, cnx):
		self.cnx = cnx
		self.cursor = cnx.cursor()
		self.cache = {}
		self._load()

	def _load(self):
		return 0

	def __contains__(self, key):
		return key.lower() in self.cache

	def __getitem__(self, key):
		try:
			return self.cache[key.lower()]
		except:
			print 'Invalid key!'

class GameCache(CacheBase):

	def _load(self):

		self.cursor.callproc('GetGameKeys')

		for _id, team1id, team2id, date in self.cursor.fetchall():
			key = str(team1id) + '_' + str(team2id) + '_' + str(date)
			key2 = str(team2id) + '_' + str(team1id) + '_' + str(date)
			if not key in self.cache:
				self.cache[key] = _id, False
			if not key2 in self.cache:
				self.cache[key2] = _id, True

class NicknameCache(CacheBase):
	sqlStr = 'SELECT ID, Nickname FROM Team'

	def _load(self):
		self.cache = {}
		self.cursor.execute(self.sqlStr)

		for _id, name in self.cursor.fetchall():
			if not name.lower() in self.cache:
				self.cache[name.lower()] = _id

		print '\nTeam id cache loaded.\n'

class GameCacheLong(CacheBase):
	#sqlStr = 'SELECT ID, location, Nickname FROM Team'

	def _load(self):
		self.cache = {}
		self.cursor.callproc('load_longformat_gameCache')

		for date, loc1, n1, loc2, n2, _id in self.cursor.fetchall():
			key1 = ' '.join([str(date), loc1, n1, loc2, n2])
			key2 = ' '.join([str(date), loc2, n2, loc1, n1])

			if not key1 in self.cache:
				self.cache[key1] = _id, False
			if not key2 in self.cache:
				self.cache[key2] = _id, True

		print '\nTeam id cache loaded.\n'

class MLB_TeamCache(CacheBase):
	sqlStr = 'SELECT Name, ID FROM MLB_Team'
	
	def _load(self):
		self.cache = {}
		self.cursor.execute(self.sqlStr)
		
		for name, _id in self.cursor.fetchall():
			if not name.lower() in self.cache:
				self.cache[name.lower()] = _id

class MLB_GameCache(CacheBase):
	sqlStr = 'SELECT Date, Team1_ID, Team2_ID, ID FROM MLB_Schedule' # change to left join.
	str = 'SELECT Date, Team1, Team2, ID, (case when outcome_id is null then true else false end) FROM MLB_Schedule LEFT JOIN MLB_Outcome ON ID = GameID'
	
	def _load(self):
		self.cache = {}
		self.cursor.execute(self.sqlStr)
		
		for date, t1, t2, _id in self.cursor.fetchall():
			key1 = ' '.join(str(date), t1, t2)
			key2 = ' '.join(str(date), t2, t1)
			if not key1.lower() in self.cache:
				self.cache[key1.lower()] = _id, False
			if not key2.lower() in self.cache:
				self.cache[key2.lower()] = _id, False



'''
cnx = MySQLdb.connect(host='', port=3306, passwd='gamera@1234',
					user='bets', db='bets')
nc = MLB_GameCache(cnx)

print nc.cache
#test = '2014-11-01 Atlant Hawks Indiana Pacers'
test = 'pirates'
print test in nc
print nc[test]



'''
