class Team():

	@classmethod
	def blankTeam(self):
		self.name = ''
		self.location = ''
		self.players = []
	
	def __init__(self, name, location, players):
		self.name = name
		self.location = location
		self.players = players
		
	
class BettingLine():

	#def __init__(self):
		#self.favortiy = Team()
		#self.game = Game()
		#self.spread = 0.0
		#self.moneyline = MoneyLine()

	def __init__(self, game, favorite, spread, moneyline):
		self.game = game
		self.favorite = favorite
		self.spread = spread
		self.moneyline = moneyline

	
class MoneyLine():

	def __init__(self, team1_ML, team2_ML):
		self.team1_ML = team1_ML
		self.team2_ML = team2_ML
		
	team1_ML = -1
	team2_ML = -1
	
class Game():
	
	def __init__(self, team1, team2):
		self.team1 = team1
		self.team2 = team2