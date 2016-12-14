import math
import random
import operator
import itertools

from .data_provider import get_status_updates
from .feature_extraction import extract_features, extract_features_batch
from .training import train_classifier, create_classifier
from .evaluation import evaluate


START_BATCH_SIZE = 50


def analyze_status_updates(user_status_updates, ext_status_updates,
                           classifier_type):
    # Extract features
    user_features = extract_features_batch(user_status_updates)
    ext_features = extract_features_batch(ext_status_updates)

    # Build labels
    user_labels = [True] * len(user_features)
    ext_labels = [False] * len(ext_features)

    # Train classifier iteratively
    start = 0
    end = START_BATCH_SIZE
    classifier = create_classifier(classifier_type)
    while end < len(user_status_updates):  # TODO handle case, if user has less than START_BATCH_SIZE tweets
        print("Train model with window size %s to %s" % (start, end))

        # Train model with status updates in window (start to end)
        samples = user_features[start:end] + ext_features
        labels = user_labels[start:end] + ext_labels
        classifier.train_iteratively(samples, labels)

        # Predict for remaining status updates
        predictions = classifier.predict(user_features[end:]).tolist()  # TODO shuffle with external tweets for evaluation

        # Extend status update window by safe zone (first x status updates
        # that were classified as written by the user)
        safe_zone_length = len(predictions)
        if False in predictions:
            safe_zone_length = predictions.index(False)

        if safe_zone_length == 0:
            return False
        else:
            # Move window
            start = end
            end = start + safe_zone_length

    return True


def prepare_data(data_provider_type, **kwargs):
    # Get status updates
    status_updates = get_status_updates(data_provider_type, **kwargs)

    # TODO For testing limit status_updates to 100 most active authors
    resources_counts_per_author = {k: len(list(g)) for k, g in itertools.groupby(status_updates, lambda x: x.author)}
    top_authors = dict(sorted(resources_counts_per_author.items(), key=operator.itemgetter(1), reverse=True)[:100]).keys()
    status_updates = [resource for resource in status_updates if resource.author in top_authors]

    return status_updates


def run_pipeline(status_updates, classifier_type):
    # Split dataset into testing and training set (per author)
    train_status_updates = []
    test_status_updates = []
    status_updates_per_author = {k: list(g) for k, g in itertools.groupby(status_updates, lambda x: x.author)}
    for author_status_updates in status_updates_per_author.values():
        random.shuffle(author_status_updates)

        train_sample_count = math.ceil(len(author_status_updates) * 0.8)
        train_status_updates += author_status_updates[:train_sample_count]
        test_status_updates += author_status_updates[train_sample_count:]

    # Extract features from train and test dataset
    train_features = [extract_features(tweet) for tweet in train_status_updates]
    test_features = [extract_features(tweet) for tweet in test_status_updates]

    # Train & evaluate classifiers
    results = []
    for author in status_updates_per_author.keys():
        train_labels = [tweet.author == author for tweet in train_status_updates]
        test_labels = [tweet.author == author for tweet in test_status_updates]

        model = train_classifier(train_features, train_labels, classifier_type)
        result = evaluate(model, test_features, test_labels)

        results.append(result)

    # Aggregate and print result
    agg_results = [sum(x) for x in zip(*results)]

    return agg_results
