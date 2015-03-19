
import requests


class TeamScraper():
	
	teamUrl = 'http://api.cbssports.com/fantasy/players/list?version=3.0&SPORT=basketball'
	playerUrl = 'http://api.cbssports.com/fantasy/pro-teams?version=3.0&SPORT=basketball'

	def Run(self):
		# Get teams and players
		teams = requests.get(self.teamUrl)
		players = requests.get(self.playerUrl)
		
		print teams.text

ts = TeamScraper()
ts.Run()