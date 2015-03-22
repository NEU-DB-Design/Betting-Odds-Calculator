import twitter
import requests
import MySQLdb

#keys

#consumer_key = 'cq8PD1TGT4K5WEii5y1hv40eN'
#consumer_secretkey = 'FG3DVXsoGAnZVH1Rue9Tt0mGINkE2blmndRUnnhsgV4zJGmie6'
#creds = 'cq8PD1IGT4K5WEii5y1hv40en:FG3DVXsoGAnZVHlRue9Tt0mGINkE2blmndRUnnhsgV4zJGmie6'
#creds64 = 'Y3E4UEQxSUdUNEs1V0VpaTV5MWh2NDBlTjpGRzNEVlhzb0dBblpWSGxSdWU5VHQwbUdJTmtFMmJsbW5kUlVubmhzZ1Y0ekpHbWllNg=='
#access_token = '3029425445-iaDKMiorBcXa2MZENCSCATfM3TPaBoFFXNb0uYZ'
#access_token_secret = 'bMIa9MSoKykERLJthUPYz0JyJ1BqpVDhxBpWa6kUrjCsA'

#url = 'https://api.twitter.com/oauth2/token'
#headers = { 'Authorization: Basic' : creds64,
#'grant_type: ' : 'client_credentials' }
#data = {'grant_type' : 'client_credentials' }
#r = requests.post(url, data=data, headers=headers)
#print (r.text)
#'''

cnx = MySQLdb.connect(host='localhost',port=3306, passwd='gamera@1234',user='bets',db='bets')
cursor = cnx.cursor()

api = twitter.Api(consumer_key='cq8PD1IGT4K5WEii5y1hv40eN', consumer_secret = 'FG3DVXsoGAnZVHlRue9Tt0mGINkE2blmndRUnnhsgV4zJGmie6', access_token_key='3029425445-iaDKMiorBcXa2MZENCSCATfM3TPaBoFFXNb0uYZ', access_token_secret='bMIa9MSoKykERLJthUPYz0JyJ1BqpVDhxBpWa6kUrjCsA')

users = api.GetFriends()
msgs = api.GetSearch(term='lebron james')

f = open('output','w')



m1 = msgs[0]

retweets =  m1.retweet_count
Favorites = m1.favorite_count
Date = m1.created_at
Tweet = m1.text
print retweets
print Favorites
print Date
print Tweet

data = (Tweet,Date, retweets, 0)

print '\n'
print 'TYPE: ' + str(type(Tweet))

add_tweet = u'''INSERT INTO Tweet
		(content, date_posted, num_retweets, num_replies)
		VALUES (%s, %s, %s, %s);'''
#add_tweet =("INSERT INTO Tweet "
		#"(content, date_posted, num_retweets, num_replies) "
		#"VALUES ('fake tweet bitch', '', 2, 3);")		


cursor.execute(add_tweet,data)
#cursor.execute(add_tweet)
cnx.commit()

'''
for m in msgs:
	unic = unicode("\n-----Tweet-----\n" + m.text + "\n")
	f.write(unic.encode('utf-8'))
'''
