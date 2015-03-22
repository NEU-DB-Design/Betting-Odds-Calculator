import pymysql
 
#db = pymysql.connect(host="localhost", port=3306, user="root", passwd="grah9033", db="mydb")
try:
	db = pymysql.connect(host="54.88.34.236", port=3306, user="bets", passwd="gamera@1234", db="bets")
except Exception, e:
	print str(e)
 
#cur = db.cursor()
#cur.execute("SELECT * FROM team")
#row = cur.fetchall()
 
#print row