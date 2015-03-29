import MySQLdb

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
