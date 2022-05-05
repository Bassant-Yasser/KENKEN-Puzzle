from itertools      import product, permutations
from functools      import reduce
from random         import random, shuffle, randint, choice
from utils          import *


def Board_generator(size):
    """ Generate a random Kenken puzzle of size size x size.
    Args:
        size (int):  The size of the puzzle.

    Returns:
        dict_board: A dictionary of (j, i) : value
        final_board: A list of tuples (j, i)
    """
    board = []                      # list of tuples (j, i) 
    for j in range(size):           # for each row of the board
        board.append([])            # add a new row
        for i in range(size):       # for each column
            board[j].append(((i + j) % size) + 1 )  # add a new cell to the row
            
    for _ in range(size):           # for each row in the board
        shuffle(board)              # shuffle the row

    for c1 in range(size):          # for each column in the board
        for c2 in range(size):      # for each column in the board
            if random() > 0.5:      # if the random number is greater than 0.5
                for r in range(size):   # for each row in the board
                    board[r][c1], board[r][c2] = board[r][c2], board[r][c1] # swap the cells
    dict_board = {}                 # dictionary of (j, i) : value
    for j in range(size):           # for each row in the board
        for i in range(size):       # for each column
            dict_board[(j + 1, i + 1)] = board[i][j] # add the cell to the dictionary

    final_board = sorted(dict_board.keys(), key=lambda var: var[1]) # sort the keys by column
    return dict_board, final_board  # return the dictionary and the board

def Generate_groups(size):
    """ Generate list of groups for a Kenken puzzle of size size x size.

    Args:
        size (int):  The size of the puzzle.

    Returns:
        groups_puzzle: A list of tuples (members, operator, target)
    """
    # uncaged is a list of tuples (j, i) 
    # dict_board is a dictionary of (j, i) : value
    dict_board, uncaged = Board_generator(size)
    
    groups_puzzle = []              # list of tuples (members, operator, target)
    while uncaged:                  # while there are uncaged cells
        groups_puzzle.append([])        # add a new group
        csize = randint(1, 4)           # generate random number 1,2,3,4
        cell = uncaged[0]               # pick a cell
        uncaged.remove(cell)            # remove it from uncaged
        groups_puzzle[-1].append(cell)  # add it to the group
        for _ in range(csize - 1):      # 0 <= _ < csize -1
            adjs = []                       # list of adjacent cells
            for other_cell in uncaged:      # for each other cell
                if Adjacent_value(cell, other_cell):    # if it is adjacent
                    adjs.append(other_cell)             # add it to the adjacents list
            if not adjs:                    # if there are no adjacent cells left to choose from
                break                       # break out of the loop
            
            cell = choice(adjs)             # pick a random adjacent cell from the list
            uncaged.remove(cell)            # remove it from uncaged
            groups_puzzle[-1].append(cell)  # add it to the group 
            
        csize = len(groups_puzzle[-1])  # csize is the number of cells in the last group
        if csize == 1:                  # if the group is a single cell
            cell = groups_puzzle[-1][0]     # get that cell
            groups_puzzle[-1] = ((cell, ), '.', dict_board[cell]) # set the group to a single cell
            continue
        elif csize == 2:                # if the group is a pair of cells
            fst, snd = groups_puzzle[-1][0], groups_puzzle[-1][1]   # get the first and second cells
            # if the first cell is divisible by the second cell
            if dict_board[fst] / dict_board[snd] > 0 and not dict_board[fst] % dict_board[snd]: 
                operator = choice("+-*/")       # pick any random operator
            else:
                operator = choice("+-*")        # pick any random operator
        else:
            operator = choice("+*")         # pick any random operator
        
        values = []                         # list of values for the group
        for cell in groups_puzzle[-1]:      # for each cell in the group
            values.append(dict_board[cell]) # add the value of the cell to the list
        target = reduce(operators[operator], values)    # calculate the target value
        # set the group to the tuple (members, operator, target)
        groups_puzzle[-1] = (tuple(groups_puzzle[-1]), operator, int(target)) 
    return groups_puzzle                    # return the groups_puzzle

