from flask import Flask, request, render_template, redirect, url_for

import uuid
import random
from expiringdict import ExpiringDict

from core.data_provider import get_status_updates
from core import StatusUpdateAnalyzer

CLASSIFIER_TYPE = "perceptron"
SCALE_FEATURES = True
EXT_TYPE = "fth"
EXT_PATH = "data/follow_the_hashtag_usa.csv"
FOREIGN_USER_ID = "steppschuh192"

app = Flask(__name__)
session_cache = ExpiringDict(10, 1200)


@app.route("/", methods=["GET"])
@app.route("/check/", methods=["GET"])
def index():
    return render_template("check.html")


@app.route("/check/", methods=["POST"])
def check_redirect():
    user_id = request.values.get("user_id")
    return redirect(url_for("check", user_id=user_id))


@app.route("/check/<user_id>", methods=["GET", "POST"])
def check(user_id):
    # Get form data
    sid = request.values.get("sid")
    confident_tweet_ids = request.values.getlist("confident_tweet_id")

    # Get results
    if sid and sid in session_cache:
        # Restore session from cache
        analyzer, result = session_cache[sid]
    else:
        # Run analyzer
        analyzer, result = analyze(user_id)

    # Refine model, if confident tweets are provided
    suspected_tweets = sorted_suspected_tweets(result)
    if confident_tweet_ids:
        result = refine(analyzer, suspected_tweets, confident_tweet_ids)
        suspected_tweets = sorted_suspected_tweets(result)

    # Store result in cache
    sid = sid or str(uuid.uuid4())
    session_cache[sid] = (analyzer, result)

    # Render template depending on result
    if suspected_tweets:
        suspected_ids = [str(x.id) for x in suspected_tweets]
        return render_template("check_compromised.html",
                               suspected_ids=suspected_ids,
                               user_id=user_id,
                               sid=sid)
    else:
        return render_template("check_success.html")


def analyze(user_id):
    # Retrieve status updates
    user_status_updates = get_status_updates("twitter", user_id=user_id)
    ext_status_updates = get_status_updates(EXT_TYPE, dataset_path=EXT_PATH)

    # Add some tweets from another user for testing purposes
    foreign_tweets = get_status_updates("twitter", user_id=FOREIGN_USER_ID)
    test_tweets = random.sample(foreign_tweets, 100)
    user_status_updates += test_tweets

    # Analyze tweets
    analyzer = StatusUpdateAnalyzer(user_status_updates,
                                    ext_status_updates,
                                    CLASSIFIER_TYPE,
                                    SCALE_FEATURES)
    result = analyzer.analyze()

    return analyzer, result


def refine(analyzer, suspected_tweets, confident_tweet_ids):
    confident_tweet_ids = list(map(int, confident_tweet_ids))
    confident_tweets = [tweet for tweet in suspected_tweets
                        if tweet.id in confident_tweet_ids]
    result = analyzer.refine(suspected_tweets, confident_tweets)

    return result


def sorted_suspected_tweets(result):
    return [x for (x, y) in sorted(result, key=lambda x: x[1])]


@app.template_filter("min")
def min_filter(l):
    return min(l)


if __name__ == "__main__":
    app.run()
