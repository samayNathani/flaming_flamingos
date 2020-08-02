import configurations
import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream
import re
from tweepy import OAuthHandler


ranked_tweets = []
location_markers = ['st.', 'st', 'av', 'avenue', 'road', 'park', 'lane', 'ln', 'l.n.', 'street', 'corner', "road", 'rd', 'highway', 'freeway']
time_markers = ["hrs", "a.m", "a.m.","m.m", "p.m.", "am", "pm", "morning", "evening", "afternoon", "now", "night"]
date_markers = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"
                "today", "tomorrow", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
police_markers = ["police", "feds", "blue", "cops", "pepper spray", "shot", "gun"]
medical_and_supplies_markers = ['doctor', 'doctors', 'nurse', 'paramedics', 'ambulance', 'hospital', 'supply', 'supplies', 'milk', 'water', 'mask']


retweets_id = []

class tweetGetter(StreamListener):
    def on_error(self, status_code):
        print(status_code)

    def on_data(self, raw_data):
        #xyz = raw_data._json
        #iden = xyz['id']
        score = 0
        tweet_content = raw_data.split()  # separate tweet content by whitespace
        for word in tweet_content:
            if word.lower() in location_markers:
                score += 1
            if word.lower() in time_markers:
                score += 1
            if word.lower() in date_markers:
                score += 1
            if word.lower() in police_markers:
                score += 1
            if word.lower() in medical_and_supplies_markers:
                score += 1

        if score >= 3:
            identity = re.findall('\"created_at\":\".{1,30}\",\"id\":\d*,\"id_str\":\"(\d*)\"', raw_data)[0]

            print(identity)
            try:
                if identity not in retweets_id:
                    api.retweet(id=identity)
                    retweets_id.append(identity)
            except:
                print('')


if __name__ == "__main__":
    listener = tweetGetter()
    auth = tweepy.OAuthHandler(configurations.api_key, configurations.api_secret_key)
    print("Go to the following URL to login")
    print(auth.get_authorization_url())
    verify = input("Enter verification code")
    token = auth.get_access_token(verifier=verify)
    mycreds = {
        'consumer_key': configurations.api_key,
        'consumer_secret': configurations.api_secret_key,
        'access_token': token[0],
        'access_token_secret': token[1]
    }
    t_auth = tweepy.OAuthHandler(
        consumer_key=mycreds['consumer_key'],
        consumer_secret=mycreds['consumer_secret']
    )
    t_auth.set_access_token(
        mycreds['access_token'],
        mycreds['access_token_secret']
    )
    stream = Stream(auth, listener)
    api = tweepy.API(t_auth, parser=tweepy.parsers.JSONParser())
    stream.filter(track=['#blm'])





#followers = api.followers()
#for tweet in api.search(q="#chicagoprotests", lang="en", rpp=10000):
#    xyz = tweet._json
#    iden = xyz['id']
#   score = 0
#   tweet_content = xyz['text'].split()  # separate tweet content by whitespace
#   for word in tweet_content:
#       if word.lower() in location_markers:
#           score += 1
#       if word.lower() in time_markers:
#           score += 1
#       if word.lower() in date_markers:
#           score += 1
#       if word.lower() in police_markers:
#           score += 1


    #engagement_and_informative_score = ((xyz['favourites_count'] / xyz["followers_count"]) + (score / 4)) / 2
    #score = engagement_and_informative_score
#    ranked_tweets.append((iden, score))

#ranked_tweets.sort(key=lambda x: x[1], reverse=True)
#counter = 0

#for i in range(10):
#   print(ranked_tweets[i][0])
#   try:
#       api.retweet(id=ranked_tweets[i][0])
 #   except:
#      continue


#only take tweets relevant from the last half hour
    #extract the tweet id to be the variable name
    #check if all the parameters are present, if they are add them to the relevant
    #member function then update score by one
    #add the tweet_class to our tweets list
    #rank tweet class by score, highest score to lowest
    #every 5 minutes, grab the most relevant tweet, retweet it then remove it from our list
    #update list every half hour
    #before retweeting, have a bad word list, and if any word in the tweet is in the bad words then remove that tweet
    #from our list, if the tweet is clean retweet it

