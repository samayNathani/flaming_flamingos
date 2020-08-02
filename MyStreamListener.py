import tweepy
import json
import time
import sys
import os

# override tweepy.StreamListener
from tweepy import API

yas = []
listemp = []
factors = []


class MyStreamListener(tweepy.StreamListener):

    def __init__(self, api=None):
        super(MyStreamListener, self).__init__(api)
        self.api = api or API()
        self.counter = 0

        # researcher ID and searchID

    def on_status(self, status):
        self.counter += 1
        yas.append(status)
        temp = (self.counter) - 1
        tweet = str(yas[temp])
        test = tweet.split(", ")

        for s in test:
            if (s.startswith("id=")):
                tweetid = s.split("=")
                yasid = str(tweetid[1])
                break
        for s in test:
            if (s.startswith("name=")):
                name = s.split("=")
                yasname = (name[1])[2:-1]
                break
        for s in test:
            if ("media_url" in s):
                mediaurl = s.split("https")
                yasurl = str((mediaurl[2])[1:-1])
                listemp.append(yasid)
                listemp.append(yasname)
                listemp.append("https:" + yasurl)
                break

        # This is the number of collected tweets stored in each json file
        if self.counter >= 50:
            print(listemp)
            quit()

    def on_error(self, status):
        print(status)
