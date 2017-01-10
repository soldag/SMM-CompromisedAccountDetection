from sklearn.ensemble import IsolationForest


class IsolationForestClassifier:
    def __init__(self):
        self.pos_features = []
        self.classifier = IsolationForest()

    def train(self, pos_samples, neg_samples):
        self.pos_features = pos_samples

        self._train()

    def train_iteratively(self, pos_samples, neg_samples):
        self.pos_features += pos_samples

        self._train()

    def _train(self):
        self.classifier = self.classifier.fit(self.pos_features)

    def predict(self, samples):
        return [p == 1 for p in self.classifier.predict(samples)]
