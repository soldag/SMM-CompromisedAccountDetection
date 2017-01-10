from sklearn import linear_model

from ..feature_extraction import extract_features_batch


class PerceptronClassifier:
    def __init__(self):
        self.classes = [True, False]
        self.classifier = linear_model.Perceptron()

    def train(self, pos_samples, neg_samples):
        features = pos_samples + neg_samples
        labels = [True] * len(pos_samples) + [False] * len(neg_samples)

        self.classifier = self.classifier.fit(features, labels)

    def train_iteratively(self, pos_samples, neg_samples):
        features = pos_samples + neg_samples
        labels = [True] * len(pos_samples) + [False] * len(neg_samples)

        self.classifier = self.classifier.partial_fit(features, labels,
                                                      classes=self.classes)

    def predict(self, samples):
        return self.classifier.predict(samples).tolist()
