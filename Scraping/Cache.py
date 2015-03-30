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
		# Init cache
		#self.cache = {}

		# Call proc
		#cnx, cursor = self.GetCursor()
		self.cursor.callproc('GetGameKeys')
		
		# Create a key for each team
		for _id, team1id, team2id, date in self.cursor.fetchall():
			key = str(team1id) + '_' + str(team2id) + '_' + str(date)
			key2 = str(team2id) + '_' + str(team1id) + '_' + str(date)
			#print 'key to check: ' + key 
			if not key in self.cache:
				self.cache[key] = _id, False
			if not key2 in self.cache:
				self.cache[key2] = _id, True

class NicknameCache():
	sqlStr = 'SELECT ID, Name FROM Team'

	def __init__(self, cnx):
		self.cnx = cnx
		self.cursor = cnx.cursor()
		self._Load()

	def _Load(self):
		self.cache = {}
		self.cursor.execute(self.sqlStr)

		for _id, name in self.cursor.fetchall():
			if not name.lower() in self.cache:
				self.cache[name.lower()] = _id

		print '\nTeam id cache loaded.\n'

	def Has(self, key):
		return key.lower() in self.cache

	def Get(self, key):
		try:
			return self.cache[key.lower()]
		except Exception, e:
			print 'Cache error:  ' + str(e)


cnx = MySQLdb.connect(host='', port=3306, passwd='gamera@1234',
					user='bets', db='bets')
nc = NicknameCache(cnx)
print nc.Has('Knicks'.lower())
print nc.Get('Celtics'.lower())
