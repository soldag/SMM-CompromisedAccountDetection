from sklearn import linear_model


class PerceptronClassifier:
    def __init__(self, classes):
        self.classes = classes
        self.classifier = linear_model.Perceptron()

    def train(self, samples, labels):
        self.classifier = self.classifier.fit(samples, labels)

    def train_iteratively(self, samples, labels):
        self.classifier = self.classifier.partial_fit(samples, labels,
                                                      classes=self.classes)

    def predict(self, sample):
        return self.classifier.predict(sample)
