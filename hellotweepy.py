import tweepy
import tokens
from detect_face import detect_face


auth = tweepy.OAuthHandler(tokens.api_key, tokens.api_secret_key)
auth.set_access_token(tokens.access_token, tokens.secret_access_token)

api = tweepy.API(auth)
search_results = api.search(q="#protest filter:images", count=100)
for tweet in search_results:
        media = tweet.entities.get('media', [])
        if len(media) != 0:
                detect_face(media[0]['media_url'])
        #print(media)