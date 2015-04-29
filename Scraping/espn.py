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
from bs4 import BeautifulSoup
import requests
import DB
import Cache
from datetime import datetime

class Espn():
	
	insertSql = 'INSERT INTO  `bets`.`MLB_BettingLine` (`GameID`, `ML1`, `ML2`, `Total`, `TML1`, `TML2`, `RunLine`, `RML1`, `RML2`) VALUES (%s,  %s,  %s,  %s,  %s,  %s,  %s,  %s, %s);'
	url = 'http://espn.go.com/mlb/lines'
	BL_map = {'BETONLINE.ag', 
		  '5Dimes.eu', 
		  'SportsBetting.ag', 
		  'BOVADA', 
		  'Fantasy911.com'}
	
	def __init__(self):
		cnx, cur = DB.GetCursor(local=True)
		self.TeamCache = Cache.MLB_TeamCache(cnx)
		self.NameCache = Cache.MLB_NameCache(cnx)
		self.GameCache = Cache.MLB_TodaysGame(cnx)
	
	def Run(self, debug=False):
		r = requests.get(self.url)
		soup = BeautifulSoup(r.text)

		table = soup.find('table', 'tablehead')
		trs = table.findAll('tr')
		
		date = None

		for tr in trs:
			if not tr.attrs:
				continue
			cls = ' '.join(tr.attrs['class'])

			print cls
			if cls == 'stathead':
				_id, switch = self.Parse_Stathead(tr.find('td').text)
				#adf = raw_input('\ntype some shit please\n')
			elif _id != None and cls != 'colhead':
				self.Parse_DataRow(_id, switch, tr)

	def Total(self, total):
		return float(total.split(' ')[0])

	def MoneyLine(self, mL):
		spt = mL.split(' ')
		ml1 = int(filter(lambda x: x.isdigit(), spt[1]))
		ml2 = int(spt[2])
		return ml1, ml2

	def Spread(self, spr):
		size = len(spr.strip())
		return float(spr[0 : size/2] )

	def Parse_DataRow(self, _id, switch, row):

		print '\n'

		tds = row.findAll('td', recursive=False)

		site = tds[0].text

		if 'injuries' in site.lower() or 'starting pitchers' in site.lower():
			return None
		if len(tds) < 2:  # Empty row
			return None

		print "Site: " + str(site)

		moneyline = tds[1].text

		#import pdb; pdb.set_trace()
		cols = tds[2].findAll('td', {u'width': u'50%'})
		total = cols[0].text
		totalML = cols[1].text

		cols2 = tds[3].findAll('td')
		runline = cols2[0].text
		runline_ML = cols2[1].text

		print 'ML: ' + moneyline
		print 'Runline: ' + runline
		print 'Total: ' + total
		print 'Total ML: ' + totalML

		#rL = self.


		t = self.Total(total)
		mL1, mL2 = self.MoneyLine(moneyline)
		tML1, tML2 = self.MoneyLine(totalML)
		rL = self.Spread(runline)
		run_ML1, run_ML2 = self.MoneyLine(runline_ML)

		# If team1/team2 is opposite of the representation in the DB,
		# switch all the values.
		if switch:
			mL1, mL2 = mL2, mL1
			tML1, tML2 = tML2, tML1
			rL *= -1
			run_ML1, run_ML2 = run_ML2, run_ML1
		
		cnx, cursor = DB.GetCursor(local=False)
		cursor.execute(self.insertSql, (_id, mL1, mL2, t, tML1, tML2, rL, run_ML1, run_ML2))
		cnx.commit()
		open('espn_dump.txt', 'a').write('\nWrote outcome for game ID: ' + str(_id))

		print 'ML parsed: ' + str(mL1) + str(mL2)
		print 'Total parsed: ' + str(t)
		print 'Total ML parsed: ' + str(tML1) + str(tML2)
		print 'Runline parsed: ' + str(rL)
		print 'Runline ML parsed: ' + str(run_ML1) + str(run_ML2)

		return ''

	def Parse_Stathead(self, head):
		#import pdb; pdb.set_trace()
		print head
		spls = head.split(',')
		trm = self.TrimAll(spls)
		print trm

		# Split words by space, strip them, and remove any city abbreviations
		#import pdb; pdb.set_trace()
		fun = lambda x: x.lower() != 'la' and x.lower() != 'ny'
		teamWords = [i.strip() for i in trm[0].split(' ') if fun(i)]

		print teamWords
		
		# Find which list item is 'at'
		if 'at' in teamWords:
			index = teamWords.index('at')
		else:
			return None

		# Get team words and seperate them by spaces
		# IE: ['red', 'sox', 'at', 'pittsburgh'] -> 'red sox', 'pittsburgh'
		firstTeam = ' '.join(teamWords[0:index]).strip()
		secondTeam = ' '.join(teamWords[index+1 : len(teamWords)]).strip()

		time = trm[1].split(' ')[0]

		print 'team 1: ' + firstTeam
		print 'team 2: ' + secondTeam
		print 'time: ' + time + '\n'

		#print self.TeamCache.cache
		if firstTeam in self.TeamCache:
			t1_id = self.TeamCache[firstTeam]
		elif firstTeam in self.NameCache:
			t1_id = self.NameCache[firstTeam]
		else:
			print 'Team 1 cache miss!'
			return None, None

		if secondTeam in self.TeamCache:
			t2_id = self.TeamCache[secondTeam]
		elif secondTeam in self.NameCache:
			t2_id = self.NameCache[secondTeam]
		else:
			print 'Team 2 cache miss!'
			return None, None

		today = datetime.now().strftime("%Y-%m-%d")
		key1 = ' '.join(str(i) for i in [today, t1_id, t2_id])
		key2 = ' '.join(str(i) for i in [today, t2_id, t1_id])

		print 'key1: ' + key1
		print 'key2: ' + key2

		in1 = key1 in self.GameCache
		in2 = key2 in self.GameCache
		print 'key1: ' + str(in1)
		print 'key2: ' + str(in2)
		
		#if not in1 and not in2:
			#import pdb; pdb.set_trace()

		if in1:
			return self.GameCache[key1]
		if in2:
			return self.GameCache[key2]
		else:
			return None, None
		

	def SplitAt(self, item, fun, once=True, include=False):
		accum = []
		for i, c in enumerate(item):
			#import pdb; pdb.set_trace()
			res = fun(c)
			if once and res and include:
				return item[0:i], item[i:len(item)]
	
	def TrimAll(self, lst):
		return map(lambda x: x.strip(), lst)

e = Espn()
e.Run(debug=True)
