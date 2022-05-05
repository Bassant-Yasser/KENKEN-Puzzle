from random         import random, shuffle, randint, choice

# lambda functions dict for operators
operators={
'+': lambda a, b: a + b,
'-': lambda a, b: a - b,
'*': lambda a, b: a * b,
'/': lambda a, b: a / b,
'.': lambda a:a
} 

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



