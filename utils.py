from random         import random, shuffle, randint, choice

# lambda functions dict for operators
operators={
'+': lambda a, b: a + b,
'-': lambda a, b: a - b,
'*': lambda a, b: a * b,
'/': lambda a, b: a / b,
'.': lambda a:a
} 

identity = lambda x: x

def shuffled(iterable):
    """Randomly shuffle a copy of iterable."""
    items = list(iterable)
    shuffle(items)
    return items

def argmin_random_tie(seq, key=identity):
    """Return a minimum element of seq; break ties at random."""
    return min(shuffled(seq), key=key)

def first(iterable, default=None):
    """Return the first element of an iterable or the next element of a generator; or default.
    
    Args:
        iterable (iterable):  The iterable to return the first element of.
        default (object):  The default value to return if the iterable is empty.
    Returns:
        object: The first element of the iterable or the next element of a generator; or default.
    """
    try:        # try to get the first element of the iterable
        return iterable[0]  # return the first element of the iterable
    except IndexError:      # if the iterable is empty
        return default      # return the default value
    except TypeError:       # if the iterable is not an iterable
        return next(iterable, default)  # return the next element of the generator or default


def count(seq):
    """Count the number of items in sequence that are interpreted as true."""
    return sum(bool(x) for x in seq)

def Adjacent_value(xy1, xy2):
    """ Return True iff the two cells are adjacent.

    Args:
        xy1  (tuple of ints (j, i)):  The first cell.
        xy2  (tuple of ints (j, i)):  The second cell.

    Returns:
        bool: True iff the two cells are adjacent.
    """
    x1, y1 = xy1        # get the first cell
    x2, y2 = xy2        # get the second cell

    dx, dy = x1 - x2, y1 - y2   # get the difference in x and y
    
    # return True iff the two cells are adjacent
    return (dx == 0 and abs(dy) == 1) or (dy == 0 and abs(dx) == 1)    



