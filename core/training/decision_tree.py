from sklearn import tree


class DecisionTreeClassifier:
    def __init__(self):
        self.samples = []
        self.labels = []
        self.classifier = tree.DecisionTreeClassifier()

    def train(self, samples, labels):
        self.samples = samples
        self.labels = labels

        self._train()

    def train_iteratively(self, samples, labels):
        self.samples += samples
        self.labels += labels

        self._train()

    def _train(self):
        self.classifier = self.classifier.fit(self.samples, self.labels)

    def predict(self, sample):
        return self.classifier.predict(sample)
