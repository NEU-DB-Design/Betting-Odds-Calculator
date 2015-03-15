# -*- coding: utf-8 -*-

import requests
from BeautifulSoup import BeautifulSoup
import unicodedata


##
## Odds Scraper Class 
##
class OddsScraper():

	url = 'http://www.vegas.com/gaming/sportsline/basketball/'
	
		
	def Run(self):
		r = requests.get(self.url)
		soup = BeautifulSoup(r.text)
		stats_table = soup.find('table', {"class" : "sportsline"})
		#print len(stats_table)
		#return
		
		tr_groups = self.Split(stats_table)
		#print len(tr_groups)
		#print len(tr_groups[0])
		#print tr_groups[0][0]
		self.Dump(str(stats_table))
		return True

	def Dump(self, text):
		open('dump', 'w').write(text)
		
	def Chuncks(self, trs):
		for i in xrange(0, len(trs), 7):
			if (i+n < len(trs)):
				yield trs[i:i+n]
			else:
				yield trs[i:len(trs)-1]
	
	def Test(self):
		#str = '½'
		print unicodedata.numeric(u'½')
	
	def Split(self, table_html):
		all_trs = table_html.find('tr')
		print 'all_trs length:  ' + str(len(all_trs))
		del all_trs[0]
		del all_trs[1]
		
		
		#return self.Chuncks(all_trs)

		'''
			for i in xrange(0, len(all_trs), 7):
			if (i+n < len(all_trs):
				yield all_trs[i:i+n]
			else:
				yield all_trs[i:len(all_trs)-1]
		
		sections = []
		current = []
		for i, tr in enumerate(all_trs):
			if i % 7 != 0:
				current.append(tr)
			else:
				sections.append(current)
				current = []
		return sections
		'''
			
		
	def Parse_Game_Section(self, html):
		trs = html.find('tr')
		tds1 = trs[2].find('td', {'nowrap' :'nowrap'})
		tds2 = trs[3].find('td')
		odds = tds2[1:3]
		tds3 = trs[4].find('td')
		moneylines = tds2[1:3]
		return tds1
		
	# Structure:
	# first tr:  2nd td with 'nowwrap' attribute are home and away team. First one is date then time.
	# second tr: tds 1-3 have spreads (0 indexed)
	# third tr: tds 1-3 have moneyline
	
	# trs
	# 0-1 -> bad (header)
	# 2-9 -> info

scraper = OddsScraper()
scraper.Test()
#scraper.Run()
print 'Success'