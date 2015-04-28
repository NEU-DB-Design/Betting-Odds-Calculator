from urllib2 import Request, urlopen, URLError
import xml.etree.ElementTree as ET
import MySQLdb

cnx = MySQLdb.connect(host='', port=3306, passwd='gamera@1234', user='bets', db='bets')
cursor = cnx.cursor()

add_player = ("INSERT INTO MLB_Player "
           "(CBS_PlayerID, name, CBS_TeamID) "
           "VALUES (%s, %s, %s)")
request = Request('http://api.cbssports.com/fantasy/players/list?version=3.0&SPORT=baseball')

try:
        response = urlopen(request)
        tree = ET.parse(response)
        root = tree.getroot()
        for player in root.findall('.//players/player'):
          playerID = player.attrib.get('id')
          fullname = player.find('.//fullname').text
          abbr = player.find('.//pro_team').text
         # headline = player.find('.///headline').text
         # print fullname, abbr #, headline
          data = (playerID, fullname, abbr)
          cursor.execute(add_player, data)
except URLError, e:
    print 'error:', e

cnx.commit()
cursor.close()
cnx.close()
