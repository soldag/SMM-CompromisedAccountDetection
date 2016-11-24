from .writing_style import WritingStyleFeatures


def extract_features(tweet):
    writing_style_features = WritingStyleFeatures(tweet.content).get_features()

    return writing_style_features
