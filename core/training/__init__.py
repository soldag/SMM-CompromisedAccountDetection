from .decision_tree import DecisionTreeClassifier
from .perceptron import PerceptronClassifier

TYPE_CLASSIFIER_MAPPING = {
    'decision_tree': DecisionTreeClassifier,
    'perceptron': PerceptronClassifier
}


def train_classifier(samples, labels, classifier_type):
    if len(samples) != len(labels):
        raise ValueError('Number of samples has to equal number of labels!')
    if classifier_type not in TYPE_CLASSIFIER_MAPPING:
        raise ValueError('Invalid classifier_type!')

    classifier = TYPE_CLASSIFIER_MAPPING[classifier_type]()
    return classifier.train(samples, labels)


def create_classifier(classifier_type):
    if classifier_type not in TYPE_CLASSIFIER_MAPPING:
        raise ValueError('Invalid classifier_type!')

    return TYPE_CLASSIFIER_MAPPING[classifier_type]()
