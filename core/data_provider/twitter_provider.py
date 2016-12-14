import csv
import json
import tweepy
from .status_update import StatusUpdate


class TwitterProvider:
    def __init__(self):
        self.client = None

    def get_status_updates(self, user_id=None,
                           dataset_path=None, tweet_limit=0):
        if user_id:
            return self._get_api_status_updates(user_id, tweet_limit)
        if dataset_path:
            return self._get_dataset_status_updates(dataset_path)

        raise ValueError('Either user_id or dataset_path has to be provided')

    def _get_api_status_updates(self, user_id, limit):
        client = self._get_twitter_client()
        tweets = tweepy.Cursor(client.user_timeline, id=user_id).items(limit)
        status_updates = [self._parse_tweet(tweet) for tweet in tweets
                          if not hasattr(tweet, 'retweeted_status')]

        return status_updates

    @staticmethod
    def _get_dataset_status_updates(dataset_path):
        status_updates = []
        with open(dataset_path, 'r', encoding='utf8') as dataset_file:
            csv_reader = csv.DictReader(dataset_file)
            for row in csv_reader:
                status_updates.append(StatusUpdate.from_dict(row))

        return status_updates

    def _get_twitter_client(self):
        if self.client is None:
            with open('twitter_credentials.json') as credentials_file:
                json_content = credentials_file.read()
                credentials = json.loads(json_content)['credentials']

                auth = tweepy.AppAuthHandler(credentials['consumer_key'],
                                             credentials['consumer_secret'])
                self.client = tweepy.API(auth)

        return self.client

    @staticmethod
    def _parse_tweet(tweet):
        return StatusUpdate(tweet.id,
                            tweet.user.screen_name,
                            tweet.text,
                            tweet.created_at,
                            tweet.lang,
                            tweet.place.country if tweet.place else None,
                            tweet.geo['coordinates'][0] if tweet.geo else None,
                            tweet.geo['coordinates'][1] if tweet.geo else None,
                            tweet.retweet_count,
                            tweet.favorite_count)
