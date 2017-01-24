from sklearn import linear_model


class PerceptronClassifier:
    def __init__(self):
        self.classes = [True, False]
        self.classifier = linear_model.Perceptron(penalty='l1', alpha=0.0008)

    def train(self, pos_samples, neg_samples, pos_weights=None):
        features = pos_samples + neg_samples
        labels = [True] * len(pos_samples) + [False] * len(neg_samples)
        weights = self._get_weights(pos_weights, pos_samples, neg_samples)

        self.classifier = self.classifier.fit(features, labels, weights)

    def train_iteratively(self, pos_samples, neg_samples, pos_weights=None):
        features = pos_samples + neg_samples
        labels = [True] * len(pos_samples) + [False] * len(neg_samples)
        weights = self._get_weights(pos_weights, pos_samples, neg_samples)

        self.classifier = self.classifier.partial_fit(features, labels,
                                                      classes=self.classes,
                                                      sample_weight=weights)

    def predict(self, samples):
        return self.classifier.predict(samples).tolist()

    def get_scores(self, samples):
        return self.classifier.decision_function(samples).tolist()

    def _get_weights(self, pos_weights, pos_samples, neg_samples):
        pos_weights = pos_weights or [1] * len(pos_samples)
        neg_weights = [1] * len(neg_samples)

        return pos_weights + neg_weights
