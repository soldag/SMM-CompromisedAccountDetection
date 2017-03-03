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
        syntactic_features = self.char_frequencies(self.PUNCTUATIONS)
        structural_features = [self.number_of_lines(),
                               self.number_of_sentences()]

        return lexical_character_features + lexical_word_features + syntactic_features + structural_features

    def number_of_chars(self):
        return len(self.text)

    def number_of_chars_of_class(self, class_characters):
        return len([1 for c in self.text if c in class_characters])

    def char_frequencies(self, class_characters):
        return [self.text.lower().count(c) for c in class_characters]

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
