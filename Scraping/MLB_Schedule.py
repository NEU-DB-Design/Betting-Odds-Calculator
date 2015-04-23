import requests
import json
import DB
import Cache
from datetime import datetime
import dateutil.parser


url = 'https://erikberg.com/mlb/results/pittsburgh-pirates.json'
headers = {'Authorization': 'Bearer afe75781-fd12-4a0a-ac3e-7c60abe05199'}

class MLB_Schedule():

	con, cursor = DB.GetCursor(local=True)
	teamCache = Cache.MLB_TeamCache(con)
	gameCache = Cache.MLB_GameCache(con)
	dbg = ''

	def Run(self):

		# Make API request
		r = requests.get(url, headers=headers)

		# Attempt to parse JSON
		try:
			decoded = json.loads(r.text)
		except:
			print 'JSON error.'
			return
		print 'JSON parsed succesfully.'
	
		# Iterate through each game entry in JSON
		for d in decoded:

			# Parse JSON fields for 1st team, 2nd team, date, and 
			# game status
			t1 = d['team']['last_name']
			t2 = d['opponent']['last_name']
			full = d['event_start_date_time']
			completed = d['event_status']

			# Init new MLB game object.
			game = MLB_Game(t1, t2, full, completed)

			# Validate/Populate team ID fields
			if not game.ValidateTeams(self.teamCache):
				print 'Team cache miss!'
				continue
			
			# Check what we have for this game.
			status = game.CheckStatus(self.gameCache)


			

			'''

			print t1
			print t2 
	
			if t1 in self.teamCache and t2 in self.teamCache:
				t1_id = self.teamCache[t1]
				t2_id = self.teamCache[t2]
			else:
				return

			print completed + '\n'

			#if completed == 'completed' and not comp
	

			try:
				yourdate = dateutil.parser.parse(full)		
			except Exception, e:
				print 'Date parse error: ' + str(e)
				continue

			gameKey1 = ' '.join([str(full), str(t1_id), str(t2_id)])
			gameKey2 = ' '.join([str(full), str(t2_id), str(t1_id)])

			need_to_switch = False
			if gameKey1 in self.gameCache:
				gameID, need_to_switch = self.gameCache[gameKey1]
			elif gameKey2 in self.gameCache:
				gameID, need_to_switch = self.gameCache[gameKey2]

			#if gameAlready exists and has data retur
			
			# if game exsists and doesn't have res and this is completed
			# add res
			
			# if not in dict at all add row
			#else:
				#print 'Game cache miss!'
				#return

			if need_to_switch:
				t1_id, t2_id  = t2_id, t1_id

			print 'Date:\n' + str(yourdate.month)
			print yourdate.day
			print yourdate.year
	
			print 'Time:\n' + str(yourdate.hour)
			print yourdate.minute
			#dt = datetime.strptime( date, "%Y-%m-%dT%H:%M:%S" )
	
			print full + '\n'
			#print time 
			#dt = datetime.strptime(date, 'yyyy-MM-ddTHH:mm:ss hh:mm')
			'''

class MLB_Game():

	Team1 = ''
	Team2 = ''
	Date = None
	IsComplete = False
	t1_id = None
	t2_id = None
	
	def __init__(self, t1, t2, d, ic):
		self.Team1 = t1
		self.Team2 = t2
		self.Date = d
		self.IsComplete = ic
		
	def ValidateTeams(self, teamCache):
		if self.Team1 in teamCache and self.Team1 in teamCache:
			self.t1_id = teamCache[self.Team1]
			self.t2_id = teamCache[self.Team2]
			return True
		else:
			return False

	##
	## Returns:
	## -1 -> No game or outcome
	##  0 -> No outcome
	##  1 -> Has both
	##
	def CheckStatus(self, gameCache):
		gameKey1 = ' '.join([str(self.Date), str(self.t1_id), str(self.t2_id)])
		gameKey2 = ' '.join([str(self.Date), str(self.t2_id), str(self.t1_id)])
		need_to_switch, has_outcome = False, None

		if gameKey1 in gameCache:
			self.gameID, need_to_switch, has_outcome = gameCache[gameKey1]
		elif gameKey2 in gameCache:
			self.gameID, need_to_switch, has_outcome = gameCache[gameKey2]
			self._SwitchTeams()
		else:
			return -1

		if has_outcome == None:
			return 1
		else:
			return 0


	def _SwitchTeams(self):
		self.t1_id, self.t2_id = self.t2_id, self.t1_id 


	

ms = MLB_Schedule()
ms.Run()
