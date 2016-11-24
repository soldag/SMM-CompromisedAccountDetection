from sklearn import tree


def train_classifier(samples, labels):
    classifier = tree.DecisionTreeClassifier()
    classifier = classifier.fit(samples, labels)

    return classifier
