from .data_provider import get_status_updates
from .feature_extraction import extract_features, extract_features_batch
from .training import train_classifier, create_classifier


START_BATCH_SIZE = 100


def analyze_status_updates(user_status_updates, ext_status_updates,
                           classifier_type):
    # Raise error if user has not enough status updates for analysis
    if len(user_status_updates) <= START_BATCH_SIZE:
        raise ValueError("Number of status updates not sufficient.")

    # Train classifier iteratively
    start = 0
    end = START_BATCH_SIZE
    suspected_status_updates = []
    classifier = create_classifier(classifier_type)
    while end < len(user_status_updates):
        # Train model with status updates in window (start to end)
        print("Train model with window size %s to %s" % (start, end))
        if start == 0:
            classifier.train_iteratively(user_status_updates[start:end],
                                         ext_status_updates)
        else:
            classifier.train_iteratively(user_status_updates[start:end], [])

        # Predict for remaining status updates
        predictions = classifier.predict(user_status_updates[end:])

        # Extend status update window by safe zone (first x status updates
        # that were classified as written by the user)
        safe_zone_length = _index(predictions, False, len(predictions))

        # Move window
        if safe_zone_length == 0:
            num_false_predictions = _index(predictions, True, len(predictions))
            suspected_status_updates += [user_status_updates[end + i]
                                         for i in range(num_false_predictions)]
            start = end + num_false_predictions
            end = start + _index(predictions[:num_false_predictions], False,
                                 len(predictions) - num_false_predictions - 1) + 1
        else:
            start = end
            end = start + safe_zone_length

        # Predict suspected status updates again with new model
        if suspected_status_updates:
            predictions = classifier.predict(suspected_status_updates)
            suspected_status_updates = [suspected_status_updates[i]
                                        for i in range(len(suspected_status_updates))
                                        if not predictions[i]]

    return suspected_status_updates


def _index(iterable, value, default_value=None):
    if value in iterable:
        return iterable.index(value)

    return default_value
