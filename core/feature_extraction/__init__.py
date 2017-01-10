from sklearn import preprocessing

from .writing_style import WritingStyleFeatures
from .meta_data import MetaDataFeatures


def extract_features(resource):
    writing_style_features = WritingStyleFeatures(resource.content).get_features()
    meta_data_features = MetaDataFeatures(resource).get_features()
    features = writing_style_features + meta_data_features

    return list(map(float, features))


def extract_features_batch(resources, scale=True):
    features = [extract_features(resource) for resource in resources]
    if scale and resources:
        features = preprocessing.scale(features).tolist()

    return features
