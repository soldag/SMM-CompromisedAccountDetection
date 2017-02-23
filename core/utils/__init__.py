import math
import itertools
from random import sample


def flatten(l):
    return [item for sublist in l for item in sublist]


def random_insert_seq(lst, seq, proportion=1):
    seq = sample(seq, min(len(seq), math.ceil(proportion * len(lst))))
    insert_locations = sample(range(len(lst) + len(seq)), len(seq))
    inserts = dict(zip(insert_locations, seq))
    input = iter(lst)
    lst[:] = [inserts[pos] if pos in inserts else next(input)
              for pos in range(len(lst) + len(seq))]
    return lst, seq


def normalize(lst, absolute=False):
    if absolute:
        lst = [abs(x) for x in lst]
    min_value = min(lst)
    max_value = max(lst)
    if min_value == max_value:
        return lst

    return [(value - min_value) / (max_value - min_value)
            for value in lst]


def split_by_author(status_updates, exclude_authors=None):
    if exclude_authors is None:
        exclude_authors = []

    authors = list(set([status_update.author for status_update in status_updates
                        if status_update.author not in exclude_authors]))
    boundary = math.ceil(len(authors) / 2)
    training_authors = authors[:boundary]
    testing_authors = authors[boundary:]
    training_status_updates = [x for x in status_updates
                               if x.author in training_authors]
    testing_status_updates = [x for x in status_updates
                              if x.author in testing_authors]

    return training_status_updates, testing_status_updates
