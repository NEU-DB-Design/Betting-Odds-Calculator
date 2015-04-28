'''
Copyright (c) <2015> <Hunt Graham, Mike Kozicky, Daniel Solomon>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''


from urllib2 import Request, urlopen, URLError
import xml.etree.ElementTree as ET
import MySQLdb

cnx = MySQLdb.connect(host='', port=3306, passwd='gamera@1234', user='bets', db='bets')
cursor = cnx.cursor()

add_team = ("INSERT INTO MLB_Team "
           "(location,Name, CBS_TeamID) "
           "VALUES (%s, %s, %s)")
#cursor.execute(add_team)

request = Request('http://api.cbssports.com/fantasy/pro-teams?version=3.0&SPORT=baseball')



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

cnx.commit()
cursor.close()
cnx.close()
