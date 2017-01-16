from sklearn import tree


class DecisionTreeClassifier:
    def __init__(self):
        self.pos_features = []
        self.neg_features = []
        self.classifier = tree.DecisionTreeClassifier()

    def train(self, pos_samples, neg_samples):
        self.pos_features = pos_samples
        self.neg_features = neg_samples

        self._train()

    def train_iteratively(self, pos_samples, neg_samples):
        self.pos_features += pos_samples
        self.neg_features += neg_samples

        self._train()

    def _train(self):
        features = self.pos_features + self.neg_features
        labels = [True] * len(self.pos_features) + \
                 [False] * len(self.neg_features)
        self.classifier = self.classifier.fit(features, labels)

    def predict(self, samples):
        return self.classifier.predict(samples).tolist()

    def get_scores(self, samples):
        return self.classifier.predict_proba(samples)[:,0].tolist()
