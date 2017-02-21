from sklearn.feature_selection import VarianceThreshold

from .data_provider import get_status_updates
from .feature_extraction import extract_features, extract_features_batch
from .training import train_classifier, create_classifier


START_BATCH_SIZE = 100
CONFIDENT_WEIGHT = 5


class StatusUpdateAnalyzer:
    def __init__(self, user_statuses, ext_statuses,
                 classifier_type, scale_features=True):
        # Raise error if user has not enough status updates for analysis
        if len(user_statuses) <= START_BATCH_SIZE:
            raise ValueError("Number of status updates not sufficient.")

        self.user_statuses = user_statuses
        self.ext_statuses = ext_statuses
        self.scale_features = scale_features
        self.result = []
        self.confident_true_statuses = []
        self.confident_false_statuses = []

        # Create classifier
        self.classifier = create_classifier(classifier_type)

        # Extract features
        all_statuses = user_statuses + ext_statuses
        all_features = extract_features_batch(all_statuses, scale_features)
        all_features = VarianceThreshold().fit_transform(all_features).tolist()
        self.user_features = all_features[:len(user_statuses)]
        self.ext_features = all_features[len(user_statuses):]

    @property
    def suspicious_statuses(self):
        return [x.status_update
                for x in sorted(self.result, key=lambda x: x.score)]

    @property
    def can_refine(self):
        suspicious_ids = set(x.id for x in self.suspicious_statuses)
        confident_false_ids = set(x.id for x in self.confident_false_statuses)
        return suspicious_ids != confident_false_ids

    def analyze(self):
        start = 0
        end = START_BATCH_SIZE
        suspicious_indices = []
        while end < len(self.user_statuses):
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

            # Predict suspicious status updates again with new model
            if suspicious_indices:
                suspicious_features = self._sublist(self.user_features,
                                                    suspicious_indices)
                suspicious_predictions = self.classifier.predict(suspicious_features)
                suspicious_indices = [suspicious_indices[i]
                                      for i in range(len(suspicious_indices))
                                      if not suspicious_predictions[i]]

            # Extend status update window by safe zone (first x status updates
            # that were classified as written by the user)
            safe_zone_length = self._index(predictions, False, len(predictions))

            # Move window
            if safe_zone_length == 0:  # next element is predicted to be suspicious
                num_false_predictions = self._index(predictions, True, len(predictions))
                suspicious_indices += [end + i for i in range(num_false_predictions)]
                start = end + num_false_predictions
                end = start + self._index(predictions[:num_false_predictions], False,
                                          len(predictions) - num_false_predictions - 1) + 1
            else:
                start = end
                end = start + safe_zone_length

        self._set_result(self.user_statuses, self.user_features,
                         suspicious_indices)

    def refine(self, confident_true_statuses, confident_false_statuses):
        self.confident_true_statuses += confident_true_statuses
        self.confident_false_statuses += confident_false_statuses

        # Train with higher weight
        confident_features = self._get_features(self.confident_true_statuses)
        compromised_features = self._get_features(self.confident_false_statuses)
        self.classifier.train_iteratively(confident_features,
                                          compromised_features,
                                          CONFIDENT_WEIGHT)

        # Predict for suspicious status updates with refined model
        suspicious_features = self._get_features(self.suspicious_statuses)
        predictions = self.classifier.predict(suspicious_features)
        suspicious_indices = [i for i in range(len(predictions))
                              if self._is_suspicious(self.suspicious_statuses[i],
                                                     predictions[i])]

        self._set_result(self.suspicious_statuses, suspicious_features,
                         suspicious_indices)

    def _get_features(self, status_updates):
        indices = [i for i, x in enumerate(self.user_statuses) if x in status_updates]
        return self._sublist(self.user_features, indices)

    def _is_suspicious(self, status_update, prediction):
        # Already marked as own status?
        if status_update in self.confident_true_statuses:
            return False

        # Already marked as external status?
        if status_update in self.confident_false_statuses:
            return True

        return not prediction

    def _set_result(self, status_updates, features, suspicious_indices):
        suspicious_scores = []
        suspicious_status_updates = []
        if suspicious_indices:
            suspicious_status_updates = self._sublist(status_updates, suspicious_indices)
            suspicious_features = self._sublist(features, suspicious_indices)
            suspicious_scores = [x for x in self.classifier.get_scores(suspicious_features)]

        self.result = [SuspiciousStatusUpdate(*tuple)
                       for tuple in zip(suspicious_status_updates, suspicious_scores)]

    @staticmethod
    def _index(iterable, value, default_value=None):
        if value in iterable:
            return iterable.index(value)

        return default_value

    @staticmethod
    def _sublist(l, indices):
        return [l[i] for i in indices]


class SuspiciousStatusUpdate:
    def __init__(self, status_update, score):
        self._status_update = status_update
        self._score = score

    @property
    def status_update(self):
        return self._status_update

    @property
    def score(self):
        return self._score
