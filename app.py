from flask import Flask
from flask import request
from flask import render_template

import uuid
import random
import urllib.parse as url_parser
from expiringdict import ExpiringDict

from core.data_provider import get_status_updates
from core import StatusUpdateAnalyzer

CLASSIFIER_TYPE = 'perceptron'
SCALE_FEATURES = True

app = Flask(__name__)
session_cache = ExpiringDict(10, 600)


@app.route('/check/', methods=['GET'])
def check():
    # Get query parameter
    sid = request.args.get('sid')
    user_url = request.args.get('account_url')
    confident_tweet_ids = request.args.getlist('select-tweet-checkbox')

    if not user_url:
        return render_template('check.html')

    if not sid or not confident_tweet_ids:
        # Retrieve status updates
        parsed_url = url_parser.urlparse(user_url)
        user_id = parsed_url.path.split('/')[1]
        user_status_updates = get_status_updates('twitter', user_id=user_id)
        ext_status_updates = get_status_updates('fth', dataset_path="data/follow_the_hashtag_usa.csv")

        # Add some tweets from another user for testing purposes
        foreign_tweets = get_status_updates('twitter', user_id='steppschuh192')
        test_tweets = random.sample(foreign_tweets, 100)
        user_status_updates += test_tweets

        # Analyze tweets
        analyzer = StatusUpdateAnalyzer(user_status_updates,
                                        ext_status_updates,
                                        CLASSIFIER_TYPE,
                                        SCALE_FEATURES)
        result = analyzer.analyze()
    else:
        # Restore session from cache
        analyzer, result = session_cache[sid]
        suspected_tweets = list(zip(*result))[0]

        # Refine model
        confident_tweet_ids = list(map(int, confident_tweet_ids))
        confident_tweets = [tweet for tweet in suspected_tweets
                            if tweet.id in confident_tweet_ids]
        result = analyzer.refine(suspected_tweets, confident_tweets)

    # Store result in cache
    sid = sid or str(uuid.uuid4())
    session_cache[sid] = (analyzer, result)

    # Render template depending on result
    if result:
        suspected_tweets = [x for (x, y) in sorted(result, key=lambda x: x[1])]
        suspected_ids = [str(x.id) for x in suspected_tweets]
        return render_template('check_compromised.html',
                               suspected_ids=suspected_ids,
                               url=user_url,
                               sid=sid)
    else:
        return render_template('check_success.html')


@app.template_filter('min')
def min_filter(l):
    return min(l)


if __name__ == '__main__':
    app.run()
