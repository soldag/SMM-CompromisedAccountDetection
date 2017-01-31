from random import sample


def flatten(l):
    return [item for sublist in l for item in sublist]


def random_insert_seq(lst, seq):
    insert_locations = sample(range(len(lst) + len(seq)), len(seq))
    inserts = dict(zip(insert_locations, seq))
    input = iter(lst)
    lst[:] = [inserts[pos] if pos in inserts else next(input)
              for pos in range(len(lst) + len(seq))]
    return lst
