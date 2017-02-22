import uuid
from random import sample
from expiringdict import ExpiringDict
from flask import Flask, request, render_template, redirect, url_for

from core import StatusUpdateAnalyzer, START_BATCH_SIZE
from core.data_provider import get_status_updates
from core.utils import random_insert_seq

CLASSIFIER_TYPE = "perceptron"
SCALE_FEATURES = True
EXT_TYPE = "fth"
EXT_PATH = "data/follow_the_hashtag_usa.csv"
FOREIGN_USER_ID = "steppschuh192"
FOREIGN_TWEET_PROPORTION = 0.05
SHOWN_TWEETS_LIMIT = 10

app = Flask(__name__)
session_cache = ExpiringDict(10, 3600)


@app.route("/", methods=["GET"])
@app.route("/check/", methods=["GET"])
def index():
    return render_template("check.html")


@app.route("/check/", methods=["POST"])
def check_redirect():
    user_id = request.values.get("user_id")
    demo = request.values.get("demo")

    return redirect(url_for("check", user_id=user_id, demo=demo))


@app.route("/check/<user_id>", methods=["GET", "POST"])
def check(user_id):
    # Get form data
    sid = request.values.get("sid")
    confident_tweet_ids = request.values.getlist("confident_tweet_id")
    demo_mode = request.values.get("demo") == '1'

    # Get results
    if sid and sid in session_cache:
        # Restore session from cache
        session = session_cache[sid]
        analyzer = session['analyzer']
        demo_mode = session['demo_mode']
    else:
        # Run analyzer
        analyzer = analyze(user_id, demo_mode)

    # Refine model, if confident tweets are provided
    if confident_tweet_ids:
        refine(analyzer, analyzer.suspicious_statuses, confident_tweet_ids)

    # Store result in cache
    sid = sid or str(uuid.uuid4())
    session_cache[sid] = {
        'analyzer': analyzer,
        'demo_mode': demo_mode
    }

    # Render template depending on result
    if analyzer.result:
        sorted_result = sorted(analyzer.result,
                               key=lambda x: x.score,
                               reverse=True)[:SHOWN_TWEETS_LIMIT]
        suspicious_ids = [str(x.status_update.id) for x in sorted_result]
        suspicious_scores = [x.score for x in sorted_result]
        return render_template("check_compromised.html",
                               sid=sid,
                               user_id=user_id,
                               demo_mode=demo_mode,
                               num_total=len(analyzer.suspicious_statuses),
                               suspicious_ids=suspicious_ids,
                               suspicious_scores=suspicious_scores,
                               can_refine=analyzer.can_refine)
    else:
        return render_template("check_success.html",
                               demo_mode=demo_mode)


def analyze(user_id, mix_foreign):
    # Retrieve status updates
    user_status_updates = get_status_updates("twitter", user_id=user_id)
    ext_status_updates = get_status_updates(EXT_TYPE, dataset_path=EXT_PATH)
    if len(ext_status_updates) > len(user_status_updates):
        ext_status_updates = sample(ext_status_updates, len(user_status_updates))

    # Add some tweets from another user for testing purposes
    if mix_foreign:
        foreign_tweets = get_status_updates("twitter", user_id=FOREIGN_USER_ID)
        mixed_status_updates = random_insert_seq(user_status_updates[START_BATCH_SIZE:],
                                                 foreign_tweets,
                                                 FOREIGN_TWEET_PROPORTION)[0]
        user_status_updates = user_status_updates[:START_BATCH_SIZE] + mixed_status_updates

    # Analyze tweets
    analyzer = StatusUpdateAnalyzer(user_status_updates,
                                    ext_status_updates,
                                    CLASSIFIER_TYPE,
                                    SCALE_FEATURES)
    analyzer.analyze()

    return analyzer


def refine(analyzer, suspicious_tweets, confident_tweet_ids):
    confident_tweet_ids = list(map(int, confident_tweet_ids))
    confident_true_tweets = [tweet for tweet in suspicious_tweets
                             if tweet.id in confident_tweet_ids]
    confident_false_tweets = [tweet for tweet in suspicious_tweets[:SHOWN_TWEETS_LIMIT]
                              if tweet.id not in confident_tweet_ids]
    analyzer.refine(confident_true_tweets, confident_false_tweets)


if __name__ == "__main__":
    app.run()
