import tweepy
import tokens

class MaxListener(tweepy.StreamListener):
    def on_data(self, raw_data):
        self.process_data(raw_data)
        return True
    def process_data(self, raw_data):
        print(raw_data)
    def on_error(self, status_code):
        if status_code == 420:
            return False

class MaxStream():
    def __init__(self, auth, listener):
        self.stream = tweepy.Stream(auth=auth,listener=listener)
    def start(self, keyword_list):
        self.stream.filter(track=keyword_list)

if __name__=="__main__":
    listener = MaxListener()

    auth = tweepy.OAuthHandler(tokens.api_key,tokens.api_secret_key)
    auth.set_access_token(tokens.access_token_key,tokens.access_token_secret)

    stream = MaxStream(auth, listener)
    stream.start("#blmprotests&#chicagoprotests")
    #stream.start("blm")