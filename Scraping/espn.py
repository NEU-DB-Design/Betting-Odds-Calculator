from bs4 import BeautifulSoup
import requests
import DB
import Cache
from datetime import datetime

class Espn():
	
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
				date = self.Parse_Stathead(tr.find('td').text)
			elif date != None and cls != 'colhead':
				self.Parse_DataRow(date, tr)
				return
			#print tr

	def Total(self, total):
		return int(total.split(' ')[0])

	def MoneyLine(self, mL):
		spt = mL.split(' ')
		ml1 = int(filter(lambda x: x.isdigit(), spt[1]))
		ml2 = int(spt[2])
		return ml1, ml2

	def Spread(self, spr):
		size = len(spr.strip())
		return float(spr[0 : size/2] )

	def Parse_DataRow(self, date, row):

		print '\n'

		tds = row.findAll('td', recursive=False)

		site = tds[0].text
		print "Site: " + str(site)

		if len(tds) < 2:  # Empty row
			return None

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
		mL = self.MoneyLine(moneyline)
		tML = self.MoneyLine(totalML)
		rL = self.Spread(runline)
		run_ML = self.MoneyLine(runline_ML)
		

		print 'ML parsed: ' + str(mL)
		print 'Total parsed: ' + str(t)
		print 'Total ML parsed: ' + str(tML)
		print 'Runline parsed: ' + str(rL)
		print 'Runline ML parsed: ' + str(run_ML)


		'''
		spreads = cols[0].text
		s1, s2 = self.SplitAt(spreads, lambda x: x == '-', include=True)
		
		print spreads

		print float(s1)

		print 'spread 1: ' + s1
		print 'spread 2: ' + s2
		'''

	

		return ''

	def Parse_Stathead(self, head):
		print head
		spls = head.split(',')
		#print spls
		#trm = map(lambda x: x.strip(), spls)
		trm = self.TrimAll(spls)
		print trm

		teamWords = self.TrimAll(trm[0].split(' '))
		print teamWords
		
		if 'at' in teamWords:
			index = teamWords.index('at')
		else:
			return None

		firstTeam = ' '.join(teamWords[0:index]).strip()
		secondTeam = ' '.join(teamWords[index+1 : len(teamWords)]).strip()

		time = trm[1].split(' ')[0]

		print 'team 1: ' + firstTeam
		print 'team 2: ' + secondTeam
		print 'time: ' + time + '\n'

		#print self.TeamCache.cache
		if firstTeam in self.TeamCache:
			t1_id = self.TeamCache[firstTeam]
		elif secondTeam in self.NameCache:
			t1_id = self.NameCache[firstTeam]
		else:
			print 'Team 1 cache miss!'
			return None

		if secondTeam in self.TeamCache:
			t2_id = self.TeamCache[secondTeam]
		elif secondTeam in self.NameCache:
			t2_id = self.NameCache[secondTeam]
		else:
			print 'Team 2 cache miss!'
			return None

		today = datetime.now().strftime("%Y-%m-%d")
		key1 = ' '.join(str(i) for i in [today, t1_id, t2_id])
		key2 = ' '.join(str(i) for i in [today, t2_id, t1_id])

		print 'key1: ' + key1
		print 'key2: ' + key2
		
		## Look up game here.
		return 1 # replace this with real Game ID

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
