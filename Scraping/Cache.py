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

#cnx = MySQLdb.connect(host='', port=3306, passwd='gamera@1234',
					#user='bets', db='bets')
#nc = NicknameCache(cnx)
#print nc.Has('Knicks'.lower())
#print nc.Get('Celtics'.lower())
