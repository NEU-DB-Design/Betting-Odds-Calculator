from urllib2 import Request, urlopen, URLError
import xml.etree.ElementTree as ET
import MySQLdb
import time

cnx = MySQLdb.connect(host='', port=3306, passwd='gamera@1234', user='bets', db='bets')
cursor = cnx.cursor()

dateRecorded = time.strftime("%d/%m/%Y")

add_stats = ("INSERT INTO MLB_Pitchers "
           "(CBS_PlayerID, K, W, L, INN, ER, Position, dateRecorded) "
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
                        K = stats.findtext('.//stat[@abbr="K"]')
                        W = stats.findtext('.//stat[@abbr="W"]')
                        L = stats.findtext('.//stat[@abbr="L"]')
                        INN = stats.findtext('.//stat[@abbr="INN"]')
                        ER = stats.findtext('.//stat[@abbr="ER"]')
                        Position = stats.findtext('.//stat[@abbr="PPos"]')
                        if Position == '1B' or Position == '2B' or Position == '3B' or Position == 'SS' or Position == 'C' or Position == 'LF' or Position == 'CF' or Position == 'RF' or Position == 'OF' or Position == 'DH':
                                continue
			if not playerID:
	 			continue
			if not K:
				K = 0; 
			if not W:
				W = 0; 
			if not L:
				L = 0; 
			if not INN:
				INN = 0; 
			if not ER:
				ER = 0; 
			if not Position:
				Position = N/A
                        
                        data = (playerID, K, W, L, INN, ER, Position)
                        cursor.execute(add_stats, data)
                except Exception, e:
                        print 'exception at: ' + str(count)
                        print playerID
                        print K
                        print W
                        print L
                        print INN
                        print ER
                        print Position
except URLError, e:
    print 'error:\t' + str(e)

cnx.commit()
cursor.close()
cnx.close()
