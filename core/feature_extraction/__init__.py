from .writing_style import WritingStyleFeatures
from .meta_data import MetaDataFeatures

def extract_features(resource):
    writing_style_features = WritingStyleFeatures(resource.content).get_features()
    meta_data_features = MetaDataFeatures(resource).get_features()

    return writing_style_features + meta_data_features
