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
    url = request.args.get('account_url', '')
    if url:
        corrected_tweets_ids = request.args.getlist('select-tweet-checkbox')
        print(corrected_tweets_ids)
        parsed_url = url_parser.urlparse(url)
        user_id = parsed_url.path.split('/')[1]
        user_status_updates = get_status_updates('twitter', user_id=user_id)
        ext_status_updates = get_status_updates('fth', dataset_path="./data/follow_the_hashtag_usa.csv")

        test_tweets = random.sample(ext_status_updates, 100)
        user_status_updates += test_tweets

        result = analyze_status_updates(user_status_updates, ext_status_updates, 'perceptron')
        compromised_ids = list(map(lambda x: x.id, result))
        if result:
            return render_template('check_compromised.html', compromised_tweets=result, compromised_ids=compromised_ids, url=url)
        else:
            return render_template('check_success.html')
    else:
        return render_template('check.html')


if __name__ == '__main__':
    app.run()
