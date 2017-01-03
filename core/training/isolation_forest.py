from sklearn.ensemble import IsolationForest

from ..feature_extraction import extract_features_batch


class IsolationForestClassifier:
    def __init__(self):
        self.pos_features = []
        self.classifier = IsolationForest()

    def train(self, pos_samples, neg_samples):
        self.pos_features = extract_features_batch(pos_samples, scale=True)

        self._train()

    def train_iteratively(self, pos_samples, neg_samples):
        self.pos_features += extract_features_batch(pos_samples, scale=True)

    def _train(self):
        self.classifier = self.classifier.fit(self.pos_features)

    def predict(self, sample):
        features = extract_features_batch(sample, scale=True)
        return [p == 1 for p in self.classifier.predict(features)]
