#!/usr/bin/python

import tweepy
import json
import time
import sys
import glob
import pyodbc

server = 'localhost'
database = 'TwitterProject'
username = 'sa'
password = 'Yasbitch99.'
driver='{ODBC Driver 17 for SQL Server}'

conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+password)
cursor = conn.cursor()
# TEST db connection
cursor.execute('SELECT * FROM RESEARCHERS')

for row in cursor:
    print(row)

# read all json files
file_str = r'bdatweets_*.json'
# list of pathnames according to above regex
file_lst = glob.glob(file_str)

# process every file
for file_idx, file_name in enumerate(file_lst):
    counter = 0
    with open(file_name, 'r') as f:
        for line in f:
            if counter == 0:
				# read researcher ID from the first line
                researcherID = int(line)
                counter = counter + 1
                continue
            if counter == 1:
				# read search ID from the second line
                searchID = int(line)
                counter = counter + 1
                continue
            if line != '\n':
				# each line is a tweet json object, load it and display user id
                tweet = json.loads(line)
                
				# collect user info
                userID = tweet['user']['id']
                user_name = tweet['user']['name']
                user_description = tweet['user']['description']
                verified = tweet['user']['verified']
                protected = tweet['user']['protected']
                user_location = tweet['user']['location']
                followers_count = tweet['user']['followers_count']
                friends_count = tweet['user']['friends_count']
                created_date = tweet['user']['created_at']
                picture_url = tweet['user']['profile_image_url_https']
                
				# collect tweet info
                tweet_id = tweet['id']
                tweet_text = tweet['text']
                tweet_date = tweet['created_at']
                reply_to = tweet['in_reply_to_screen_name']
                favorite_count = tweet['favorite_count']
                reply_count = tweet['reply_count']
                retweet_count = tweet['retweet_count']
                quoted = tweet['is_quote_status']
                
				# collect hashtags info in tweets with hashtags
                hashtag_objects = tweet['entities']['hashtags']
                
                # collect places info only on tweets with places
                if tweet['place']:
                        place_id = tweet['place']['id']
                        place_type = tweet['place']['place_type']
                        place_name = tweet['place']['full_name']
                        place_country = tweet['place']['country']
                        coordinates = tweet['place']['bounding_box']['coordinates']
                
                if tweet['entities']['media']:
                        media_objects = tweet['entities']['media']
                        
				# insert only if the user doesn't exists already in the database
                # inserto user object
                rows = cursor.execute('SELECT * FROM USERS WHERE id = ?', userID).fetchall()
                if len(rows) == 0:
                    cursor.execute('''
                	    INSERT INTO USERS (id, "name", "description", verified, protected, "location", followers_count, friends_count, created_date, picture)
                		    VALUES
                			    (?,?,?,?,?,?,?,?,?,?)
                    ''', (userID, user_name, user_description, verified, protected, user_location, followers_count, friends_count, created_date, picture_url))
                    conn.commit()
                    
				# insert tweet object
                rows = cursor.execute('SELECT * FROM TWEETS WHERE id = ?', tweet_id).fetchall()
                if len(rows) == 0:
                    cursor.execute('''
					    INSERT INTO TWEETS (id, "text", "user", created, reply_to, favorite_count,reply_count, retweet_count, search_id, is_quote, media)
						    VALUES
							    (?,?,?,?,?,?,?,?,?,?)
				    ''', (tweet_id, tweet_text, userID, tweet_date, reply_to, favorite_count, reply_count, retweet_count, searchID, quoted))
                    conn.commit()
                    
				# insert hashtags
                for hashtag in hashtag_objects:
					# insert only unique hashtags
                    rows = cursor.execute('''SELECT * FROM HASHTAGS WHERE tweet_id = ? AND
							hashtag = ?''', (tweet_id, hashtag['text'])).fetchall()
                    if len(rows) == 0:
                        index_objects = hashtag['indices']
                        cursor.execute('''
                            INSERT INTO HASHTAGS (tweet_id, hashtag, index_beg, index_end)
                                VALUES(?,?,?,?)
                        ''', (tweet_id, hashtag['text'], hashtag['indices'][0], hashtag['indices'][1]))
                        conn.commit()

                # insert places
                if tweet['place']:
                    rows = cursor.execute ('SELECT * FROM PLACES WHERE id = ?', place_id).fetchall()
                    if len(rows) == 0:
                        cursor.execute('''
                            INSERT INTO PLACES (tweet_id, id, "type", "name", country, latitude, longitude)
                                VALUES
                                    (?,?,?,?,?,?,?)
                        ''', (tweet_id, place_id, place_type, place_name, place_country, coordinates[0][0][1], coordinates[0][0][0]))
                        conn.commit()
                
                
                            
                            
cursor.close()
conn.close()
