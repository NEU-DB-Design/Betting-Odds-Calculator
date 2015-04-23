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
		r = requests.get(url, headers=headers)
		#print r.text

		try:
			decoded = json.loads(r.text)
		except:
			print 'JSON error.'
			return
	
		print 'JSON parsed succesfully.'
		#print r.text
	
		for d in decoded:
			#print str(d) + '\n'
			t1 = d['team']['last_name']
			print t1
			t2 = d['opponent']['last_name']
			print t2 
	
			if t1 in self.teamCache and t2 in self.teamCache:
				t1_id = self.teamCache[t1]
				t2_id = self.teamCache[t2]
			else:
				print 'Team cache miss!'
				return

			completed = d['event_status']
			print completed + '\n'

			#if completed == 'completed' and not comp
	
			full = d['event_start_date_time']

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
		
		

ms = MLB_Schedule()
ms.Run()
