from urllib2 import Request, urlopen, URLError
import xml.etree.ElementTree as ET
import MySQLdb

cnx = MySQLdb.connect(host='', port=3306, passwd='gamera@1234', user='gsmp', db='gsmp')
cursor = cnx.cursor()

add_team = ("INSERT INTO hdm_Team2 "
           "(location,name, abbr) "
           "VALUES (%s, %s, %s)")
#cursor.execute(add_team)

request = Request('http://api.cbssports.com/fantasy/pro-teams?version=3.0&SPORT=basketball')



try:
        response = urlopen(request)
        tree = ET.parse(response)
        root = tree.getroot()
        for team in root.findall('.//pro_team'):
          nickname = team.find('nickname').text
          name = team.find('name').text
          abbr = team.find('abbr').text
          data = (name, nickname,abbr)
          #sqlStr = "INSERT INTO hdm_Team (name, location) VALUES (" + nickname + ", " + name + ')"'
          #print name, nickname, abbr
          cursor.execute(add_team, data)
          #cursor.execute(sqlStr)
except URLError, e:
    print 'error:', e
