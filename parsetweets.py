import tweepy
import json
import time
import sys
import glob
import pyodbc


def parseTweets():
    # read all json files
    file_str = r'bdatweets_*.json'
    # list of pathnames according to above regex
    file_lst = glob.glob(file_str)

    # process every file
    usernames = []
    ids = []
    mediass = []
    for file_idx, file_name in enumerate(file_lst):
        counter = 0
        with open(file_name, 'r') as f:
            for line in f:
                if counter == 0:
                    # read researcher ID from the first line
                    researcherID = line
                    counter = counter + 1
                    continue
                if counter == 1:
                    # read search ID from the second line
                    searchID = line
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

                    tweet_id = tweet['id']

                    # collect hashtags info in tweets with hashtags
                    hashtag_objects = tweet['entities']['hashtags']

                    medias = tweet['entities']
                    media_obj = medias.get('media')
                    media_links = []
                    if media_obj:
                        for media in media_obj:
                            yas = media['media_url']
                            media_links.append(yas)
                    usernames.append(user_name)
                    ids.append(tweet_id)
                    mediass.append(media_links)

    return usernames, ids, mediass