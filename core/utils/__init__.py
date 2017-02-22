import math

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
