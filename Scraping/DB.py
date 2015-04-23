import MySQLdb

def GetCursor(local=False):
		if not local:
                	cnx = MySQLdb.connect(host='', port=3306, passwd='gamera@1234',
                                        user='bets', db='bets')
		else:
                	cnx = MySQLdb.connect(host='54.88.34.236', port=3306, passwd='gamera@1234',
                                        user='bets', db='bets')
                return cnx, cnx.cursor()

t, t2 = GetCursor(local=True)
