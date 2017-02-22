from sklearn import linear_model

from core.utils import normalize


class PerceptronClassifier:
    def __init__(self):
        self.classes = [True, False]
        self.classifier = linear_model.Perceptron(penalty='l1', alpha=0.0008)

    def train(self, pos_samples, neg_samples, weight=1):
        features = pos_samples + neg_samples
        labels = [True] * len(pos_samples) + [False] * len(neg_samples)
        weights = [weight] * len(features)

        self.classifier = self.classifier.fit(features, labels, weights)

    def train_iteratively(self, pos_samples, neg_samples, weight=1):
        features = pos_samples + neg_samples
        labels = [True] * len(pos_samples) + [False] * len(neg_samples)
        weights = [weight] * len(features)

        self.classifier = self.classifier.partial_fit(features, labels,
                                                      classes=self.classes,
                                                      sample_weight=weights)

    def predict(self, samples):
        return self.classifier.predict(samples).tolist()

    def get_scores(self, samples):
        return normalize(self.classifier.decision_function(samples).tolist(),
                         absolute=True)
