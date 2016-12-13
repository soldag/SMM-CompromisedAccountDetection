import math
import random
import operator
import itertools

from .data_provider import get_status_updates
from .feature_extraction import extract_features
from .training import train_classifier
from .evaluation import evaluate


def prepare_data(data_provider_type, **kwargs):
    # Get status updates
    status_updates = get_status_updates(data_provider_type, **kwargs)

    # TODO For testing limit status_updates to 100 most active authors
    resources_counts_per_author = {k: len(list(g)) for k, g in itertools.groupby(status_updates, lambda x: x.author)}
    top_authors = dict(sorted(resources_counts_per_author.items(), key=operator.itemgetter(1), reverse=True)[:100]).keys()
    status_updates = [resource for resource in status_updates if resource.author in top_authors]

    return status_updates

def run_pipeline(data_provider_type, status_updates, classifier_type, **kwargs):
    base_size = 200
    base_status_updates = get_status_updates(data_provider_type, **kwargs) + status_updates[:base_size]
    base_features = [extract_features(tweet) for tweet in base_status_updates]
    model = train_classifier(base_features, [False] * (len(base_status_updates) - base_size) + [True] * base_size, classifier_type)
    predictions = []
    for i in range(len(status_updates[20:])):
        prediction = model.predict(extract_features(status_updates[i]))
        predictions.append(prediction)
    print(predictions)
    return 0, 0, 0, 0


def run_pipeline_old(status_updates, classifier_type):
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
