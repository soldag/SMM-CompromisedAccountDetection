from sklearn import tree


class DecisionTreeClassifier:
    def __init__(self):
        self.pos_features = []
        self.neg_features = []
        self.pos_weights = []
        self.classifier = tree.DecisionTreeClassifier()

    def train(self, pos_samples, neg_samples, pos_weights=None):
        self.pos_features = pos_samples
        self.neg_features = neg_samples
        self.pos_weights = pos_weights

        self._train()

    def train_iteratively(self, pos_samples, neg_samples, pos_weights=None):
        self.pos_features += pos_samples
        self.neg_features += neg_samples
        self.pos_weights += pos_weights or [1] * len(pos_samples)

        self._train()

    def _train(self):
        features = self.pos_features + self.neg_features
        labels = [True] * len(self.pos_features) + \
                 [False] * len(self.neg_features)
        weights = self._get_weights(self.pos_weights,
                                    self.pos_features, self.neg_features)
        self.classifier = self.classifier.fit(features, labels,
                                              sample_weight=weights)

    def predict(self, samples):
        return self.classifier.predict(samples).tolist()

    def get_scores(self, samples):
        return self.classifier.predict_proba(samples)[:,0].tolist()

    def _get_weights(self, pos_weights, pos_samples, neg_samples):
        pos_weights = pos_weights or [1] * len(pos_samples)
        neg_weights = [1] * len(neg_samples)

        return pos_weights + neg_weights
