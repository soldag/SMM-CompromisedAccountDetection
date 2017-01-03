from sklearn import tree

from ..feature_extraction import extract_features_batch


class DecisionTreeClassifier:
    def __init__(self):
        self.pos_features = []
        self.neg_features = []
        self.classifier = tree.DecisionTreeClassifier()

    def train(self, pos_samples, neg_samples):
        self.pos_features = extract_features_batch(pos_samples)
        self.neg_features = extract_features_batch(neg_samples)

        self._train()

    def train_iteratively(self, pos_samples, neg_samples):
        self.pos_features += extract_features_batch(pos_samples)
        self.neg_features += extract_features_batch(neg_samples)

        self._train()

    def _train(self):
        features = self.pos_features + self.neg_features
        labels = [True] * len(self.pos_features) + \
                 [False] * len(self.neg_features)
        self.classifier = self.classifier.fit(features, labels)

    def predict(self, sample):
        features = extract_features_batch(sample)
        return self.classifier.predict(features).tolist()
