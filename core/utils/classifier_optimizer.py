import numpy as np

from time import time, ctime
from scipy.stats import randint as sp_randint

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.feature_selection import VarianceThreshold
from sklearn import linear_model, tree

from core.feature_extraction import extract_features_batch


def prepare_two_class_data(user_statuses, ext_statuses):
    # Extract features
    all_statuses = user_statuses + ext_statuses
    all_features = extract_features_batch(all_statuses, True)
    all_features = VarianceThreshold().fit_transform(all_features).tolist()

    # Determine targets
    all_targets = [True] * len(user_statuses) + [False] * len(ext_statuses)

    return all_features, all_targets


# Utility function to report best scores
def report(results, n_top=3):
    file = open('classifier_evaluation_report.log', 'a')
    file.write("{0}:\n".format(
        ctime(int(time()))))
    for i in range(1, n_top + 1):
        candidates = np.flatnonzero(results['rank_test_score'] == i)
        for candidate in candidates:
            file.write("Model with rank: {0} # ".format(i))
            file.write("Mean validation score: {0:.3f} (std: {1:.3f}) # ".format(
                results['mean_test_score'][candidate],
                results['std_test_score'][candidate]))
            file.write("Parameters: {0}".format(results['params'][candidate]))
            file.write("\n")
    file.write("\n")
    file.close()


CLASSIFIER_MAPPING = {
    # clf - classifier
    # prep - according prepare data method
    # dist - specify parameters and distributions to sample from
    # grid - use a full grid over all parameters
    'perceptron': {
        'clf': linear_model.Perceptron,
        'prep': prepare_two_class_data,
        'dist': {
            'penalty': [None, 'l2', 'l1', 'elasticnet'],
            'alpha': [0.0001, 0.001, 0.01, 0.1, 1],
            'fit_intercept': [True, False],
            'n_iter': sp_randint(1, 20),
            'shuffle': [True, False],
            'verbose': sp_randint(1, 5),
            'eta0': [1.0, 1.5, 2.0],
            'random_state': [0, None],
            'class_weight': ['balanced', None],
            'warm_start':  [True, False]
        },
        'grid': {
            'penalty': [None, 'l2', 'l1', 'elasticnet'],
            'alpha': [0.0001, 0.0003, 0.0004, 0.0005, 0.0006, 0.0007, 0.0008, 0.0009],
            'fit_intercept': [True, False],
            'n_iter': [5, 10, 20, 30],
            'shuffle': [True, False],
            'verbose': [0, 2, 4],
            'eta0': [1.0, 1.5, 2.0],
            'random_state': [0, None],
            'class_weight': ['balanced', None],
            'warm_start':  [True, False]
        }
    },
    'decision_tree': {
        'clf': tree.DecisionTreeClassifier,
        'prep': prepare_two_class_data,
        'dist': {
            'criterion': ['gini', 'entropy'],
            'splitter': ['best', 'random'],
            'max_features': [None, 'auto', 'sqrt', 'log2'],
            'max_depth': sp_randint(1, 1000),
            'min_samples_split': sp_randint(1, 1000),
            'min_samples_leaf': [1, 4, 0.2, 0.5],
            'min_weight_fraction_leaf': [0.0, 0.5],
            'max_leaf_nodes': [None, 10, 20],
            'class_weight': [None, 'balanced'],
            'presort': [False, True]
        },
        'grid': {
            'criterion': ['gini', 'entropy'],
            'splitter': ['best', 'random'],
            'max_features': [None, 'auto', 'sqrt', 'log2'],
            'max_depth': [None, 1, 10, 100, 500, 1000],
            'min_samples_split': [2, 100, 500, 1000],
            'min_samples_leaf': [1, 100, 0.2, 0.5],
            'min_weight_fraction_leaf': [0.0, 0.3, 0.5],
            'max_leaf_nodes': [None, 10, 100, 500],
            'class_weight': [None, 'balanced'],
            'presort': [False, True]
        }
    }
}


class ClassifierOptimizer:
    def __init__(self, classifier, user_statuses, ext_statuses):
        if classifier not in CLASSIFIER_MAPPING:
            raise ValueError('Invalid classifier_type!')

        self.classifier = CLASSIFIER_MAPPING[classifier]['clf']()

        prepared_data = CLASSIFIER_MAPPING[classifier]['prep'](user_statuses, ext_statuses)
        self.data = prepared_data[0]
        self.target = prepared_data[1]

        self.param_dist = CLASSIFIER_MAPPING[classifier]['dist']
        self.param_grid = CLASSIFIER_MAPPING[classifier]['grid']

    def execute(self):
        self.randomized_search_cv()
        self.grid_search_cv()

    def randomized_search_cv(self):
        # run randomized search
        n_iter_search = 20
        random_search = RandomizedSearchCV(self.classifier, param_distributions=self.param_dist,
                                           n_iter=n_iter_search)
        start = time()
        random_search.fit(self.data, self.target)
        print("RandomizedSearchCV took %.2f seconds for %d candidates"
              " parameter settings." % ((time() - start), n_iter_search))
        report(random_search.cv_results_)

    def grid_search_cv(self):
        # run grid search
        grid_search = GridSearchCV(self.classifier, param_grid=self.param_grid)
        start = time()
        grid_search.fit(self.data, self.target)

        print("GridSearchCV took %.2f seconds for %d candidate parameter settings."
              % (time() - start, len(grid_search.cv_results_['params'])))
        report(grid_search.cv_results_)
