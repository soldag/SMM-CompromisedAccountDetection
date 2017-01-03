import random

from .data_provider import get_status_updates
from .feature_extraction import extract_features, extract_features_batch
from .training import train_classifier, create_classifier
from .evaluation import evaluate


START_BATCH_SIZE = 50


def analyze_status_updates(user_status_updates, ext_status_updates,
                           classifier_type):
    # Raise error if user has not enough status updates for analysis
    if len(user_status_updates) <= START_BATCH_SIZE:
        raise ValueError("Number of status updates not sufficient.")

    # Sort status updates by publishing date time
    user_status_updates = sorted(user_status_updates, key=lambda x: x.date_time)

    # Train classifier iteratively
    start = 0
    end = START_BATCH_SIZE
    classifier = create_classifier(classifier_type)
    false_predictions = []
    while end < len(user_status_updates):
        # Train model with status updates in window (start to end)
        print("Train model with window size %s to %s" % (start, end))
        if start == 0:
            classifier.train_iteratively(user_status_updates[start:end],
                                         ext_status_updates)
        else:
            classifier.train_iteratively(user_status_updates[start:end], [])

        # Predict for remaining status updates
        # TODO shuffle with external tweets for evaluation
        predictions = classifier.predict(user_status_updates[end:])

        # Extend status update window by safe zone (first x status updates
        # that were classified as written by the user)
        safe_zone_length = len(predictions)
        if False in predictions:
            false_predictions.append(user_status_updates[start + predictions.index(False)])
            user_status_updates.remove(user_status_updates[start + predictions.index(False)])

            # Move window to start after the false prediction
            start = start + predictions.index(False) + 1
        else:
            # Move window
            start = end

        end = start + safe_zone_length

    return false_predictions
