from sklearn.feature_selection import VarianceThreshold

from .data_provider import get_status_updates
from .feature_extraction import extract_features, extract_features_batch
from .training import train_classifier, create_classifier


START_BATCH_SIZE = 100
CONFIDENT_WEIGHT = 2


class StatusUpdateAnalyzer:
    def __init__(self, user_status_updates, ext_status_updates,
                 classifier_type, scale_features=True):
        # Raise error if user has not enough status updates for analysis
        if len(user_status_updates) <= START_BATCH_SIZE:
            raise ValueError("Number of status updates not sufficient.")

        self.user_status_updates = user_status_updates
        self.ext_status_updates = ext_status_updates
        self.scale_features = scale_features

        # Create classifier
        self.classifier = create_classifier(classifier_type)

        # Extract features
        all_status_updates = user_status_updates + ext_status_updates
        all_features = extract_features_batch(all_status_updates, scale_features)
        all_features = VarianceThreshold().fit_transform(all_features).tolist()
        self.user_features = all_features[:len(user_status_updates)]
        self.ext_features = all_features[len(user_status_updates):]

    def analyze(self):
        start = 0
        end = START_BATCH_SIZE
        suspected_indices = []
        while end < len(self.user_status_updates):
            # Train model with status updates in window (start to end)
            print("Train model with window size %s to %s" % (start, end))
            if start == 0:
                self.classifier.train_iteratively(self.user_features[start:end],
                                                  self.ext_features)
            else:
                self.classifier.train_iteratively(self.user_features[start:end],
                                                  [])

            # Predict for remaining status updates
            predictions = self.classifier.predict(self.user_features[end:])

            # Predict suspected status updates again with new model
            if suspected_indices:
                suspected_features = [self.user_features[i] for i in suspected_indices]
                suspected_predictions = self.classifier.predict(suspected_features)
                suspected_indices = [suspected_indices[i] for i in range(len(suspected_indices))
                                     if not suspected_predictions[i]]

            # Extend status update window by safe zone (first x status updates
            # that were classified as written by the user)
            safe_zone_length = self._index(predictions, False, len(predictions))

            # Move window
            if safe_zone_length == 0:  # next element is predicted to be suspicious
                num_false_predictions = self._index(predictions, True, len(predictions))
                suspected_indices += [end + i for i in range(num_false_predictions)]
                start = end + num_false_predictions
                end = start + self._index(predictions[:num_false_predictions], False,
                                          len(predictions) - num_false_predictions - 1) + 1
            else:
                start = end
                end = start + safe_zone_length

        return self._get_result(self.user_status_updates, self.user_features,
                                suspected_indices)

    def refine(self, suspected_status_updates, confident_tweets):
        # Train with confident tweets with higher weight
        confident_features = self._get_features(confident_tweets)
        confident_weights = [CONFIDENT_WEIGHT] * len(confident_features)
        self.classifier.train_iteratively(confident_features, [], confident_weights)

        # Predict for suspected status updates with refined model
        suspected_features = self._get_features(suspected_status_updates)
        predictions = self.classifier.predict(suspected_features)
        suspected_indices = [i for i in range(len(predictions))
                             if not predictions[i]]

        # Filter out confident tweets (in case of classification errors)
        suspected_indices = [i for i in suspected_indices
                             if suspected_status_updates[i] not in confident_tweets]

        return self._get_result(suspected_status_updates, suspected_features,
                                suspected_indices)

    def _get_features(self, status_updates):
        indices = [i for i, x in enumerate(self.user_status_updates) if x in status_updates]
        return self._sublist(self.user_features, indices)

    def _get_result(self, status_updates, features, suspected_indices):
        suspected_scores = []
        suspected_status_updates = []
        if suspected_indices:
            suspected_status_updates = self._sublist(status_updates, suspected_indices)
            suspected_features = self._sublist(features, suspected_indices)
            suspected_scores = self.classifier.get_scores(suspected_features)

        return list(zip(suspected_status_updates, suspected_scores))

    @staticmethod
    def _index(iterable, value, default_value=None):
        if value in iterable:
            return iterable.index(value)

        return default_value

    @staticmethod
    def _sublist(l, indices):
        return [l[i] for i in indices]