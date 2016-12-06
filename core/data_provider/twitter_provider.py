import json
import tweepy
from .status_update import StatusUpdate


def get_status_updates(user_id):
    credentials_file = open('twitter_credentials.json').read()
    credentials = json.loads(credentials_file)['credentials']

    auth = tweepy.OAuthHandler(credentials['consumer_key'], credentials['consumer_secret'])
    auth.set_access_token(credentials['access_token_key'], credentials['access_token_secret'])
    api = tweepy.API(auth)

    tweets = tweepy.Cursor(api.user_timeline, id=user_id).items()
    status_updates = [parse_tweet(tweet) for tweet in tweets]
    return status_updates


def parse_tweet(tweet):
    return StatusUpdate(tweet.id,
                        tweet.user.screen_name,
                        tweet.text,
                        tweet.created_at,
                        tweet.lang,
                        (tweet.place.country if tweet.place else None),
                        (tweet.geo['coordinates'][0] if tweet.geo else None),
                        (tweet.geo['coordinates'][1] if tweet.geo else None),
                        tweet.retweet_count,
                        tweet.favorite_count)
