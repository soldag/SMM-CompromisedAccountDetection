from sklearn import svm

from core.utils import flatten


class OneClassSvmClassifier:
    def __init__(self):
        self.pos_features = []
        self.weights = []
        self.classifier = svm.OneClassSVM(kernel='linear', nu=0.1)

    def train(self, pos_samples, neg_samples, weights=None):
        self.pos_features = pos_samples
        self.weights = weights or [1] * len(pos_samples)

        self._train()

    def train_iteratively(self, pos_samples, neg_samples, weights=None):
        self.pos_features += pos_samples
        self.weights += weights or [1] * len(pos_samples)

        self._train()

    def _train(self):
        self.classifier = self.classifier.fit(self.pos_features,
                                              sample_weight=self.weights)

    def predict(self, samples):
        return [p == 1 for p in self.classifier.predict(samples)]

    def get_scores(self, samples):
        return flatten(self.classifier.decision_function(samples).tolist())
