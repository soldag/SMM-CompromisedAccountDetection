from .writing_style import WritingStyleFeatures


def extract_features(resource):
    writing_style_features = WritingStyleFeatures(resource.content).get_features()

    return writing_style_features
