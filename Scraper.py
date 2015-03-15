# -*- coding: utf-8 -*-

import requests
from BeautifulSoup import BeautifulSoup
import unicodedata
from BettingLine import Team, BettingLine

class Scraper():
	
	url = 'http://sports.bovada.lv/sports-betting/nba-basketball-lines.jsp'
	
	def Run(self):
		r = requests.get(self.url)
		soup = BeautifulSoup(r.text)

		divs = soup.findAll('div', 'event left even')
		divs += soup.findAll('div', 'event left odd')
		
		self.Dump(divs, 'dump')

		betting_lines = []
		for i, div in enumerate(divs):
			print '\nSection: ' + str(i)
			betting_lines.append(self.ParseSection(div))
			
		print '\nCount:'
		print len(divs)
		
	def ParseSection(self, section):
		#b = BettingLine
		t = Team.blankTeam()
	
		self.Dump(section, 'indiv')

		# Find spreads
		spreads = section.findAll('a', 'lineOdd')
		if not spreads:
			spreads = section.find('div', 'line-normal').find('span', 'disabled')
		if not spreads or len(spreads) < 2:
			print 'SPREADS NOT FOUND'
		else:
			print 'spread 1: ' + spreads[0].text
			print 'spread 1: ' + spreads[1].text
		
		# Find names
		names = section.findAll('a', 'competitor left')
		if not names:
			names = section.findAll('span', 'left disabled')
		if not names or len(names) < 2:
			print 'NAMES NOT FOUND.'
		else:
			print 'Team 1: ' + names[0].text
			print 'Team 2: ' + names[1].text
			
		# Check if this has already been scraped
		# TODO
		
		# If not, add new
		b = BettingLine('', '', '', '')
		return b
		
		
	def Dump(self, text, location):
		open(location, 'w').write(str(text))
		
sraper = Scraper()
sraper.Run()