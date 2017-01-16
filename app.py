from flask import Flask
from flask import request
from flask import render_template

from core.data_provider import get_status_updates
from core import analyze_status_updates

import urllib.parse as url_parser
import random
import json

app = Flask(__name__)


@app.route('/check/', methods=['GET'])
def check():
    user_url = request.args.get('account_url', '')
    if user_url:
        # Get ids of corrected tweets from query params
        corrected_tweets_ids = request.args.getlist('select-tweet-checkbox')
        print(corrected_tweets_ids)

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
        compromised_tweets, scores = analyze_status_updates(user_status_updates, ext_status_updates, 'perceptron')
        compromised_tweets = [x for (y, x) in sorted(zip(scores, compromised_tweets))]

        # Render template depending on result
        if compromised_tweets:
            compromised_ids = [str(x.id) for x in compromised_tweets]
            return render_template('check_compromised.html',
                                   compromised_ids=compromised_ids,
                                   url=user_url)
        else:
            return render_template('check_success.html')
    else:
        return render_template('check.html')


if __name__ == '__main__':
    app.run()
