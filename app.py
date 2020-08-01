import tweepy
import tokens
from detect_face import detect_face


def app():
    api = bot()
    get_tweets(api)


def bot():
    auth = tweepy.OAuthHandler(tokens.api_key, tokens.api_secret_key)
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
    return api


def get_tweets(api):
    search_results = api.search(q="#blmprotest filter:images -filter:retweets", count=100)
    for tweet in search_results:
        user_name = tweet.user.screen_name
        id = tweet.id_str
        media = tweet.entities.get('media', [])
        if len(media) != 0:
            if detect_face(media[0]['media_url']):
                try:
                    api.update_status('@' + user_name + ' A face has been detected in this photo', id)
                except:
                    continue


if __name__ == '__main__':
    app()
