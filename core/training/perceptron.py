from sklearn import linear_model

from ..feature_extraction import extract_features_batch


class PerceptronClassifier:
    def __init__(self):
        self.classes = [True, False]
        self.classifier = linear_model.Perceptron()

    def train(self, pos_samples, neg_samples):
        pos_features = extract_features_batch(pos_samples, scale=True)
        neg_features = extract_features_batch(neg_samples, scale=True)
        features = pos_features + neg_features
        labels = [True] * len(pos_features) + [False] * len(neg_features)
        self.classifier = self.classifier.fit(features, labels)

    def train_iteratively(self, samples, labels):
        self.classifier = self.classifier.partial_fit(samples, labels,
                                                      classes=self.classes)

    def predict(self, sample):
        features = extract_features_batch(sample, scale=True)
        return self.classifier.predict(features).tolist()
