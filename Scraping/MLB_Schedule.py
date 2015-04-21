import requests

url = 'https://erikberg.com/nba/results/golden-state-warriors.json'
headers = {'Authorization': 'Bearer afe75781-fd12-4a0a-ac3e-7c60abe05199'}

def Run():
	r = requests.get(url, headers=headers)
	#print r.text
