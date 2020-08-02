import tweepy
import tokens
import json
import time
tweets = []
class MaxListener(tweepy.StreamListener):
    def on_data(self, raw_data):
        self.process_data(raw_data)
        return True
    def process_data(self, raw_data):
        iden = raw_data
        decoded_data = json.loads(raw_data) #dictionary
        tweets.append(decoded_data)
        print(decoded_data["text"])
    def on_error(self, status_code):
        if status_code == 420:
            return False

class MaxStream():
    def __init__(self, auth, listener):
        self.stream = tweepy.Stream(auth=auth,listener=listener)
    def start(self, keyword_list):
        self.stream.filter(track=keyword_list,languages=["en"], is_async=True)




if __name__=="__main__":
    listener = MaxListener()

    auth = tweepy.OAuthHandler(tokens.api_key,tokens.api_secret_key)
    auth.set_access_token(tokens.access_token_key,tokens.access_token_secret)

    stream = MaxStream(auth, listener)
    stream.start(["#blmprotests, BLM protest, protest, #neworleansprotest,#chicagoprotests"])
    while True:
        print("hello") #access list and read
        time.sleep(1)
    #stream.start("blm")
