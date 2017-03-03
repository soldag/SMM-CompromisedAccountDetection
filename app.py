import uuid
import argparse
from random import sample
from expiringdict import ExpiringDict
from flask import Flask, request, render_template, redirect, url_for

from core import StatusUpdateAnalyzer, START_BATCH_SIZE
from core.data_provider import get_status_updates
from core.utils import random_insert_seq, split_by_author

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 5000
DEFAULT_DATA_SOURCE = "twitter"
DEFAULT_DATA_PATH = "data/tweets.csv"
DEFAULT_CLASSIFIER = "decision_tree"

DEFAULT_USER_ID = "satyanadella"
SCALE_FEATURES = True
TWEET_LIMIT = 1000
SHOWN_TWEETS_LIMIT = 10

app = Flask(__name__)
app.config['data_source'] = DEFAULT_DATA_SOURCE
app.config['dataset_path'] = DEFAULT_DATA_PATH
app.config['classifier'] = DEFAULT_CLASSIFIER

session_cache = ExpiringDict(10, 3600)


@app.route("/", methods=["GET"])
def index():
    demo = request.values.get("demo")
    return redirect(url_for("check_get", demo=demo))


@app.route("/check/", methods=["GET"])
def check_get():
    demo = request.values.get("demo")
    error = request.values.get("error")
    user_id = request.values.get("user_id", DEFAULT_USER_ID)

    return render_template("check.html",
                           demo=demo, error=error, user_id=user_id)


@app.route("/check/", methods=["POST"])
def check_post():
    demo = request.values.get("demo")
    user_id = request.values.get("user_id")

    return redirect(url_for("check_user", demo=demo, user_id=user_id))


@app.route("/check/<user_id>", methods=["GET", "POST"])
def check_user(user_id):
    # Get form data
    sid = request.values.get("sid")
    confident_tweet_ids = request.values.getlist("confident_tweet_id")
    demo = request.values.get("demo")
    demo_mode = demo == '1'

    # Get results
    try:
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
    except Exception as error:
        return redirect(url_for("check_get",
                                demo=demo, user_id=user_id, error=str(error)))

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
                               demo=demo,
                               user_id=user_id,
                               num_total=len(analyzer.suspicious_statuses),
                               suspicious_ids=suspicious_ids,
                               suspicious_scores=suspicious_scores,
                               can_refine=analyzer.can_refine)
    else:
        return render_template("check_success.html", demo=demo)


def analyze(user_id, mix_foreign):
    # Retrieve status updates
    user_statuses = get_status_updates("twitter", user_id=user_id,
                                       tweet_limit=TWEET_LIMIT)
    ext_statuses = get_status_updates(app.config['data_source'],
                                      dataset_path=app.config['dataset_path'])
    ext_training_statuses, ext_testing_statuses = split_by_author(ext_statuses,
                                                                  [user_id])

    # Add some tweets from another user for testing purposes
    if mix_foreign:
        mixed_statuses = random_insert_seq(user_statuses[START_BATCH_SIZE:],
                                           ext_testing_statuses)[0]
        user_statuses = user_statuses[:START_BATCH_SIZE] + mixed_statuses

    # Analyze tweets
    if len(ext_training_statuses) > len(user_statuses):
        ext_training_statuses = sample(ext_training_statuses, len(user_statuses))
    analyzer = StatusUpdateAnalyzer(user_statuses,
                                    ext_training_statuses,
                                    app.config['classifier'],
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
    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--host",
                        help="Hostname of the app " +
                             "[default: %s]" % DEFAULT_HOST,
                        default=DEFAULT_HOST)
    parser.add_argument("-P", "--port",
                        help="Port for the app " +
                             "[default: %s]" % DEFAULT_PORT,
                        default=DEFAULT_PORT)
    parser.add_argument("-s", "--data-source",
                        help="The data source for tweets that should be used for analyzing. Possible values are 'fth', 'mp' and 'twitter' " +
                             "[default: %s]" % DEFAULT_DATA_SOURCE,
                        default=DEFAULT_DATA_SOURCE)
    parser.add_argument("-p", "--dataset-path",
                        help="The path of the dataset that should be used for analyzing " +
                             "[default: %s]" % DEFAULT_DATA_PATH,
                        default=DEFAULT_DATA_PATH)
    parser.add_argument("-c", "--classifier",
                        help="The classifier to use " +
                             "[default: %s]" % DEFAULT_CLASSIFIER,
                        default=DEFAULT_CLASSIFIER)

    args = parser.parse_args()
    app.config['data_source'] = args.data_source
    app.config['dataset_path'] = args.dataset_path
    app.config['classifier'] = args.classifier

    app.run(host=args.host, port=int(args.port))
