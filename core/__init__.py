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
