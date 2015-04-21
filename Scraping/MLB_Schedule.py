import requests
import json
import DB
import Cache
from datetime import datetime
import dateutil.parser


url = 'https://erikberg.com/mlb/results/pittsburgh-pirates.json'
headers = {'Authorization': 'Bearer afe75781-fd12-4a0a-ac3e-7c60abe05199'}

con, cursor = DB.GetCursor()

cache = Cache.MLB_GameCache(con)

def Run():
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
		print t2 + '\n'

		date1 = d['event_start_date_time'][0:19]
		#time = d['event_start_date_time'][20:22]


		date = d['event_start_date_time'][0:10]

		yourdate = dateutil.parser.parse(date)
		print yourdate.month
		print yourdate.day
		print yourdate.year
		#dt = datetime.strptime( date, "%Y-%m-%dT%H:%M:%S" )

		print date
		#print time 
		#dt = datetime.strptime(date, 'yyyy-MM-ddTHH:mm:ss hh:mm')
		
		

Run()
