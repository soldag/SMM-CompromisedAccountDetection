from nltk.util import ngrams
from nltk import word_tokenize
from collections import Counter


def extract_n_grams(resources):
    c_grams = []
    w_grams = []
    for resource in resources:
        c_grams += NGramFeatures(resource.content).get_character_grams()
        w_grams += NGramFeatures(resource.content).get_word_grams()
    c_grams_count = Counter(c_grams).most_common(50)
    w_grams_count = Counter(w_grams).most_common(50)
    c_grams = [gram_count[0] for gram_count in c_grams_count]
    w_grams = [gram_count[0] for gram_count in w_grams_count]
    return [c_grams, w_grams]


class NGramFeatures:
    N = 4

    def __init__(self, text, grams=None):
        self.text = text
        self.grams = grams

    def get_features(self):
        return self.character_n_gram_feature() + self.word_n_gram_feature()

    def character_n_gram_feature(self):
        grams_count = Counter(elem for elem in self.get_character_grams())

        return [grams_count[c_gram] for c_gram in self.grams[0]]

    def word_n_gram_feature(self):
        grams_count = Counter(elem for elem in self.get_word_grams())

        return [grams_count[w_gram] for w_gram in self.grams[1]]

    def get_character_grams(self):
        return [x for x in ngrams(self.text, self.N)]

    def get_word_grams(self):
        return [x for x in ngrams(word_tokenize(self.text), self.N)]
