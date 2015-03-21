# -*- coding: utf-8 -*-

import requests
from BeautifulSoup import BeautifulSoup
import unicodedata
from BettingLine import Team, BettingLine

class Scraper():

	def __init__(self):
		t = Team.blankTeam()
		self.teams = ['x', 'a', 'b']
		#if 'xsdf' in self.teams:
			#print 'found'
		#else:
			#print 'nope'
		#self.teamList = [
	
	#teams 
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
		t = Team.blankTeam()
	
		self.Dump(section, 'indiv')

		# Find spreads
		spreads = section.findAll('a', 'lineOdd')
		if not spreads:
			try:
				spreads = section.find('div', 'line-normal').find('span', 'disabled')
			except Exception, e: #If no line-normal found then this bet is 'suspended'
				print 'Parse Error: ' + str(e)
				return
		if not spreads or len(spreads) < 2:
			print 'SPREADS NOT FOUND'
			return None
		else:
			#print 'spread 1: ' + str(spreads[0])
			#print 'spread 1: ' + str(spreads[1])
			print 'spread 1: ' + spreads[0].text
			print 'spread 1: ' + spreads[1].text
		
		# Find names
		names = section.findAll('a', 'competitor left')
		if not names:
			names = section.findAll('span', 'left disabled')
		if not names or len(names) < 2:
			print 'NAMES NOT FOUND.'
			return None
		else:
			print 'Team 1: ' + names[0].text
			print 'Team 2: ' + names[1].text
			
		# Validate teams
		#if not self.CheckTeam(spreads[0], spreads[1]): # TODO change this to return a tuple for team 1 and 2
			#return None
		
	def CheckTeam(self, teamName):
		retrun (teamName in self.teams)
		
	def CheckLine(line):
		return True
		
	def LoadTeams(self):
		sqlString = 'SELECT * FROM TEAMS'
		return ['steelers', 'ravens', 'patriots', 'jets']
		# dal
		
	def Dump(self, text, location):
		open(location, 'w').write(str(text))
		
sraper = Scraper()
sraper.Run()