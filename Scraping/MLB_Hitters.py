from urllib2 import Request, urlopen, URLError
import xml.etree.ElementTree as ET
import MySQLdb
import time

cnx = MySQLdb.connect(host='', port=3306, passwd='gamera@1234', user='bets', db='bets')
cursor = cnx.cursor()

dateRecorded = time.strftime("%d/%m/%Y")


add_stats = ("INSERT INTO MLB_Hitters "
           "(CBS_PlayerID, Hits, HR, RBI,SB,Games,Position, dateRecorded) "
           "VALUES (%s, %s, %s, %s, %s, %s, %s, DATE_SUB(NOW(), INTERVAL 4 HOUR))")
request = Request('http://api.cbssports.com/fantasy/stats?version=3.0&timeframe=2015&period=ytd&SPORT=baseball')

try:
        response = urlopen(request)
        tree = ET.parse(response)
        root = tree.getroot()
        count = 0
        for stats in root.findall('.//player_stats/player'):
                try:
                        count += 1
                        playerID = stats.attrib.get('id')
                        Hits = stats.findtext('.//stat[@abbr="H"]')
                        HR = stats.findtext('.//stat[@abbr="HR"]')
                        RBI = stats.findtext('.//stat[@abbr="RBI"]')
			SB = stats.findtext('.//stat[@abbr="SB"]')
                        Games = stats.findtext('.//stat[@abbr="G"]')
			Position = stats.findtext('.//stat[@abbr="PPos"]')
			if Position == 'SP' or Position == 'RP' or Position == 'P':
				continue
			if not playerID:
				continue		
			if not Hits:
				Hits = 0
			if not HR: 
				HR = 0
			if not RBI: 
				RBI = 0
			if not SB: 
				SB = 0
			if not Games: 
				Games = 0
			if not Position:
				Position = N/A

                        data = (playerID, Hits, HR, RBI, SB, Games, Position)
                        cursor.execute(add_stats, data)
			players.append(playerID)
                except Exception, e:
                        print 'exception at: ' + str(count)
                        print playerID
                        print Hits
                        print HR
                        print RBI
                        print SB
			print Games
			print Position
except URLError, e:
    print 'error:\t' + str(e)

cnx.commit()
cursor.close()
cnx.close()
