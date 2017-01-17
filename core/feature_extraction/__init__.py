from sklearn import preprocessing

from .writing_style import WritingStyleFeatures
from .meta_data import MetaDataFeatures
from .n_grams import NGramFeatures, extract_n_grams


def extract_features(resource, grams):
    writing_style_features = WritingStyleFeatures(resource.content).get_features()
    meta_data_features = MetaDataFeatures(resource).get_features()
    n_gram_features = NGramFeatures(resource.content, grams).get_features()
    features = writing_style_features + meta_data_features + n_gram_features

    return list(map(float, features))


def extract_features_batch(resources, scale=True):
    grams = extract_n_grams(resources)
    features = [extract_features(resource, grams) for resource in resources]
    if scale and resources:
        features = preprocessing.scale(features).tolist()

    return features
