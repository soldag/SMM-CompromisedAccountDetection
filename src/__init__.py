import math
import random
import operator
import itertools

from .parsing import parse_dataset
from .feature_extraction import extract_features
from .training import train_classifier
from .evaluation import evaluate


def prepare_data(dataset_path, dataset_type):
    # Parse dataset
    resources = parse_dataset(dataset_path, dataset_type)

    # TODO For testing limit tweets to 100 most active authors
    resources_counts_per_author = {k: len(list(g)) for k, g in itertools.groupby(resources, lambda x: x.author)}
    top_authors = dict(sorted(resources_counts_per_author.items(), key=operator.itemgetter(1), reverse=True)[:100]).keys()
    resources = [resource for resource in resources if resource.author in top_authors]

    return resources


def run_pipeline(tweets, classifier_type):
    # Split dataset into testing and training set (per author)
    train_tweets = []
    test_tweets = []
    tweets_per_author = {k: list(g) for k, g in itertools.groupby(tweets, lambda x: x.author)}
    for author_tweets in tweets_per_author.values():
        random.shuffle(author_tweets)

        train_sample_count = math.ceil(len(author_tweets) * 0.8)
        train_tweets += author_tweets[:train_sample_count]
        test_tweets += author_tweets[train_sample_count:]

    # Extract features from train and test dataset
    train_features = [extract_features(tweet) for tweet in train_tweets]
    test_features = [extract_features(tweet) for tweet in test_tweets]

    # Train & evaluate classifiers
    results = []
    for author in tweets_per_author.keys():
        train_labels = [tweet.author == author for tweet in train_tweets]
        test_labels = [tweet.author == author for tweet in test_tweets]

        model = train_classifier(train_features, train_labels, classifier_type)
        result = evaluate(model, test_features, test_labels)

        results.append(result)

    # Aggregate and print result
    agg_results = [sum(x) for x in zip(*results)]

    return agg_results
