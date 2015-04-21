from bs4 import BeautifulSoup
import requests
import DB

class Espn():
	
	url = 'http://espn.go.com/nba/lines'
	BL_map = {'BETONLINE.ag', 
		  '5Dimes.eu', 
		  'SportsBetting.ag', 
		  'BOVADA', 
		  'Fantasy911.com'}
	
	#def __init__(self):
		#self.GameCacheLong = 
	
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
			#print tr

	def Parse_DataRow(self, date, row):

		print '\n'

		tds = row.findAll('td', recursive=False)

		print tds[0].text
		
		print len(tds)

		if len(tds) < 2:  # Empty row
			return None

		#spreads = tds[1].findAll()

		cols = tds[1].findAll('td', {u'width': u'50%'})
		
		print len(cols)

		spreads = cols[0].text

		s1, s2 = self.SplitAt(spreads, lambda x: x == '-', include=True)
		
		print spreads

		print float(s1)

		print 'spread 1: ' + s1
		print 'spread 2: ' + s2

	

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

		firstTeam = ' '.join(teamWords[0:index])
		secondTeam = ' '.join(teamWords[index+1 : len(teamWords)])

		print firstTeam
		print secondTeam + '\n'

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
