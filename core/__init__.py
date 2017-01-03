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
    # Sort status updates by publishing date time
    user_status_updates = sorted(user_status_updates, key=lambda x: x.date_time)

    # Train classifier iteratively
    start = 0
    end = START_BATCH_SIZE
    classifier = create_classifier(classifier_type)
    while end < len(user_status_updates):  # TODO handle case, if user has less than START_BATCH_SIZE tweets
        # Train model with status updates in window (start to end)
        print("Train model with window size %s to %s" % (start, end))
        if start == 0:
            classifier.train_iteratively(user_status_updates[start:end],
                                         ext_status_updates)
        else:
            classifier.train_iteratively(user_status_updates[start:end], [])

        # Predict for remaining status updates
        predictions = classifier.predict(user_status_updates[end:])  # TODO shuffle with external tweets for evaluation

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
