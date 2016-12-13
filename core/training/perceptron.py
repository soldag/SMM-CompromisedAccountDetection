from sklearn import linear_model

def train_classifier(samples, labels, classifier = None):
    classifier = classifier or linear_model.Perceptron()
    classifier = classifier.partial_fit(samples, labels, classes=labels)

    return classifier
