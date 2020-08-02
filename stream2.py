import tweepy
import tokens
import json
import time
tweets = []
auth = tweepy.OAuthHandler(tokens.api_key,tokens.api_secret_key)
auth.set_access_token(tokens.access_token_key,tokens.access_token_secret)
print("Go to the following URL to login")
print(auth.get_authorization_url())
verify = input("Enter verification code")
token = auth.get_access_token(verifier=verify)
mycreds = {
        'consumer_key': tokens.api_key,
        'consumer_secret': tokens.api_secret_key,
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
api = tweepy.API(t_auth)
class MaxListener(tweepy.StreamListener):
    def on_data(self, raw_data):
        self.process_data(raw_data)
        return True
    def process_data(self, raw_data):
        iden = raw_data
        decoded_data = json.loads(raw_data) #dictionary
        if decoded_data["user"]["followers_count"]>= 10:
            tweets.append(decoded_data)
        print(decoded_data["id"])
        
    def on_error(self, status_code):
        if status_code == 420:
            return False

class MaxStream():
    def __init__(self, auth, listener):
        self.stream = tweepy.Stream(auth=auth,listener=listener)
    def start(self, keyword_list):
        self.stream.filter(track=keyword_list,languages=["en"], is_async=True)

class Ranking():
    ranked_tweets = []
    location_markers = ['st.', 'st', 'av', 'avenue', 'road', 'park', 'lane', 'ln', 'l.n.', 'street', 'corner']
    time_markers = ["hrs", "a.m", "a.m.","m.m", "p.m.", "am", "pm", "morning", "evening", "afternoon", "now"]
    date_markers = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"
                    "today", "tomorrow", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    police_markers = ["police", "feds", "blue", "cops"]
    def check(self):
        """
        Scores the tweets based on our information criteria
        """
        for xyz in tweets:
            iden = xyz['id']
            score = 0
            tweet_content = xyz['text'].split()  # separate tweet content by whitespace
            for word in tweet_content:
                if word.lower() in self.location_markers:
                    score += 1
                if word.lower() in self.time_markers:
                    score += 1
                if word.lower() in self.date_markers:
                    score += 1
                if word.lower() in self.police_markers:
                    score += 1
            engagement_and_informative_score = ((xyz["favorite_count"] / xyz["user"]["followers_count"]) + (score / 4)) / 2
            score = engagement_and_informative_score
            self.ranked_tweets.append((iden, score))
    def retweet(self):
        """
        Calls the check function to append tweets to ranked_tweets
        Retweets the top 10 best ranked tweets 
        """
        self.check()
        self.ranked_tweets.sort(key=lambda x: x[1], reverse=True)
        for i in range(1):
            print(self.ranked_tweets[i][0])
            try:
                api.retweet(id=self.ranked_tweets[i][0])
            except:
                continue



if __name__=="__main__":
    listener = MaxListener()

    
    

    stream = MaxStream(auth, listener)
    stream.start(["#blmprotests, BLM protest, protest, #neworleansprotest,#chicagoprotests"])
    trial = Ranking()
    while True:
        time.sleep(10)
        print("Retweeting: ")
        trial.retweet()
    #stream.start("blm")