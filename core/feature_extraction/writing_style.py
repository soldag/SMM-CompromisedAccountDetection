import string
import numpy as np
from nltk.tokenize import word_tokenize, sent_tokenize


class WritingStyleFeatures:
    SPECIAL_CHARACTERS = '~ @#$%^&*-_=,+><[]{}/\|'
    PUNCTUATIONS = ',.?!:;`"'

    def __init__(self, text):
        self.text = text
        self.words = word_tokenize(self.text)
        self.sentences = sent_tokenize(self.text, language='english')

    def get_features(self):
        # Lexical features
        lexical_character_features = [self.number_of_chars(),
                                      self.number_of_chars_of_class(string.ascii_letters),
                                      self.number_of_chars_of_class(string.ascii_uppercase),
                                      self.number_of_chars_of_class(string.digits),
                                      self.number_of_chars_of_class(string.whitespace)]\
                                     + self.char_frequencies(string.ascii_lowercase)\
                                     + self.char_frequencies(self.SPECIAL_CHARACTERS)
        lexical_word_features = [self.number_of_words(),
                                 self.number_of_short_words(),
                                 self.avg_word_length(),
                                 self.avg_sentence_length_chars(),
                                 self.avg_sentence_length_words(),
                                 self.number_of_unique_word()]
        syntactic_features = self.char_frequencies(self.PUNCTUATIONS) + self.function_word_frequency()
        structural_features = [self.number_of_lines(),
                               self.number_of_sentences()]
        lexical_features = lexical_character_features + lexical_word_features + syntactic_features + structural_features

        return lexical_features

    def number_of_chars(self):
        return len(self.text)

    def number_of_chars_of_class(self, class_characters):
        return len([1 for c in self.text if c in class_characters])

    def char_frequencies(self, class_characters):
        return [self.text.count(c) for c in class_characters]

    def number_of_words(self):
        return len(self.words)

    def number_of_short_words(self):
        return len([word for word in self.words if len(word) < 4])

    def avg_word_length(self):
        return np.mean([len(word) for word in self.words])

    def number_of_unique_word(self):
        return len(set(self.words))

    def number_of_sentences(self):
        return len(self.sentences)

    def avg_sentence_length_chars(self):
        return np.mean([len(s) for s in self.sentences])

    def avg_sentence_length_words(self):
        return np.mean([len(word_tokenize(s)) for s in self.sentences])

    def number_of_lines(self):
        return len(self.text.splitlines())

    def function_word_frequency(self):
        function_words = ['a', 'between', 'in', 'nor', 'some', 'upon', 'about', 'both', 'including', 'nothing',
                          'somebody us', 'above', 'but', 'inside', 'of', 'someone', 'used', 'after', 'by', 'into',
                          'off', 'something', 'via', 'all', 'can', 'is', 'on', 'such', 'we', 'although', 'cos', 'it',
                          'once', 'than', 'what', 'am', 'do', 'its', 'one', 'that', 'whatever', 'among', 'down',
                          'latter', 'onto', 'the', 'when', 'an', 'each', 'less', 'opposite', 'their', 'where', 'and',
                          'either', 'like', 'or', 'them', 'whether', 'another', 'enough', 'little', 'our', 'these',
                          'which', 'any', 'every', 'lots', 'outside', 'they', 'while', 'anybody', 'everybody', 'many',
                          'over', 'this', 'who', 'anyone', 'everyone', 'me', 'own', 'those', 'whoever', 'anything',
                          'everything', 'more', 'past', 'though', 'whom', 'are', 'few', 'most', 'per', 'through',
                          'whose', 'around', 'following', 'much', 'plenty', 'till', 'will', 'as', 'for', 'must', 'plus',
                          'to', 'with', 'at', 'from', 'my', 'regarding', 'toward', 'within', 'be', 'have', 'near',
                          'same', 'towards', 'without', 'because', 'he', 'need', 'several', 'under', 'worth', 'before',
                          'her', 'neither', 'she', 'unless', 'would', 'behind', 'him', 'no', 'should', 'unlike', 'yes',
                          'below', 'i', 'nobody', 'since', 'until', 'you', 'beside', 'if', 'none', 'so', 'up', 'your']
        return [self.words.count(w) for w in function_words]
