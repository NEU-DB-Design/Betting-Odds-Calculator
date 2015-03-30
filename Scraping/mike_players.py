from urllib2 import Request, urlopen, URLError
import xml.etree.ElementTree as ET
import MySQLdb

cnx = MySQLdb.connect(host='localhost', port=3306, passwd='gamera@1234', user='bets', db='bets')
cursor = cnx.cursor()

SQL = 'Select * From Player'
cursor.execute(SQL)
players = cursor.fetchall()
_id, name, abbreviation = players[0]
print _id
print name
print abbreviation
print ('success!')



'''
add_player = ("INSERT INTO Player "
           "(name, abbr) "
           "VALUES (%s, %s)")
request = Request('http://api.cbssports.com/fantasy/players/list?version=3.0&SPORT=basketball')

try:
        response = urlopen(request)
        tree = ET.parse(response)
        root = tree.getroot()
        for player in root.findall('.//players/player'):
          fullname = player.find('.//fullname').text
          abbr = player.find('.//pro_team').text
         # headline = player.find('.///headline').text
         # print fullname, abbr #, headline
	  data = (fullname, abbr)
	  cursor.execute(add_player, data)
except URLError, e:
    print 'error:', e

cnx.commit()
cursor.close()
cnx.close()
'''
