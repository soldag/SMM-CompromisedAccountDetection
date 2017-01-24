import os
import csv

from core.data_provider.twitter_provider import TwitterProvider


def crawl_status_updates(output_path, user_limit=100, limit=0):
    provider = TwitterProvider()
    user_ids = list(_get_most_popular_users(user_limit))

    with open(output_path, 'w') as output_file:
        csv_writer = csv.DictWriter(output_file, [])
        user_limit = min(user_limit, len(user_ids))
        for i in range(0, user_limit):
            user_id = user_ids[i]
            print("Crawling user @%s (%i/%i)..." % (user_id, i+1, user_limit))

            # Retrieve tweets
            tweets = provider.get_status_updates(user_id, tweet_limit=limit)
            if tweets:
                # Write header to csv, if not already done
                if not csv_writer.fieldnames:
                    csv_writer.fieldnames = sorted(tweets[0].to_dict().keys())
                    csv_writer.writeheader()

                # Write tweets to csv
                csv_writer.writerows([tweet.to_dict() for tweet in tweets])


def _get_most_popular_users(limit=100):
    file_path = os.path.join(os.path.dirname(__file__),
                             'popular_twitter_users.csv')
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for i in range(0, limit):
            yield next(csv_reader)[0]
