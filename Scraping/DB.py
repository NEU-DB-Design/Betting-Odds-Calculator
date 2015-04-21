import MySQLdb

def GetCursor(self):
                cnx = MySQLdb.connect(host='', port=3306, passwd='gamera@1234',
                                        user='bets', db='bets')
                return cnx, cnx.cursor()
