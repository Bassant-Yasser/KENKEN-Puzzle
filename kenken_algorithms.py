from time           import time
from kenken_helper  import *
from utils          import *


class Kenken(): 
    """Class for Kenken puzzle."""
    def __init__(self, size, groups_puzzle):  
        """Initialize a Kenken puzzle.

        Args:
            size (int):  The size of the puzzle.
            groups_puzzle (list of lists of lists of ints):  The puzzle.
        """
        self.variables = [] # list of variables
        for var ,_,_ in groups_puzzle:  # for each group in the puzzle
            self.variables.append(var)      # add the variable to the list
        self.domains = Group_domains(size, groups_puzzle) # dict of domains for each variable
        self.neighbors = Group_neighbors(groups_puzzle)   # dict of neighbors for each variable
        self.current_domains = None                       # dict of current domains for each variable
        self.num_assignments = 0                          # number of assignments
        self.size = size                                  # size of the puzzle
        self.checks = 0                                   # number of checks
        
    def ken_support_current_domains(self):
        """Update current_domains to reflect the current domains of the variables."""
        if self.current_domains is None:    # if current_domains is None
            self.current_domains= {}        # create a new current_domains
            for v in self.variables:            # for each variable
                # add the domain to the current_domains
                self.current_domains[v] = list(self.domains[v]) 
        
    def ken_choose_domain(self, var):
        """Return the domain of var.

        Args:
            var (tuple of cells (j, i)):  The variable.

        Returns:
            list of values:  The domain.
        """
        s = set()                                 # set of values 
        # if the domains is not None and the variable is in the domains
        if self.domains and var in self.domains:    
            for v in self.domains[var]:           # for each value in the domains
                s.add(v)                          # add the value to the set
        # if the current_domains is not None and the variable is in the current_domains
        if self.current_domains and var in self.current_domains:   
            for v in self.current_domains[var]:   # for each value in the current_domains
                s.add(v)                          # add the value to the set
        return list(s)   # return the set as a list
 



# ==========================================================
# Backtracking Algorithm for solving the KenKen puzzle.
# ==========================================================
default_inference = lambda ken, var, value, assignment, removals: True  # default inference returns True

def backtracking_search(ken,
                assignment={},
                inference=default_inference):
    """Backtracking Algorithm for solving the KenKen puzzle.

    Args:
        ken (KenKen):  The KenKen instance.
        assignment (dict of assignments var : val ):  The assignment.
        inference (function):  The inference function.

    Returns:
        dict of assignments var : val ):  The assignment.
    """
    if len(assignment) == len(ken.variables):   # if the assignment is complete
        return assignment                       # return the assignment
    # select first unassigned variable
    var =first(list(set(ken.variables)-assignment.keys())) # mrv(assignment,ken)
    for value in ken.ken_choose_domain(var):    # for each value in the domain of var  #lcv(var,assignment, ken):#
        if ken.ken_nummbers_of_conflicts(var, value, assignment) == 0:  # if there is no conflict
            ken.ken_increase_assignment(var, value, assignment)         # increase the assignment
            removals = ken.ken_assumption_of_removals(var, value)       # get the removals
            if inference(ken, var, value, assignment, removals):        # if the inference is successful
                result = backtracking_search(ken,assignment,inference)  # recursive call to the backtracking_search
                if result is not None:                             # if the result is not None
                    return result                                  # return the result
            ken.ken_restore(removals)                              # restore the removals
            ken.ken_unassignment(var, assignment)                  # unassign the variable
    return None    # return None if the assignment is not complete
    
# ====================================================================
# Gather assignments
# ====================================================================
def gather(name, size, groups_puzzle):
    """Gather assignments.

    Args:
        name (str):  The name of algorithm to be used.
        size (int):  The size of the puzzle.
        groups_puzzle (list of lists of lists of int):  The puzzle.

    Returns:
        list of dict of assignments var : val ):  The assignments.
    """

    selected_algorithm = algorithms_Fn[name]    # get the algorithm  
    ken = Kenken(size, groups_puzzle)           # create the KenKen instance
    dt = time()                                 # get the current time
    assignments = selected_algorithm(ken)       # get the assignments
    dt = time() - dt                            # get the time difference
    dt = float("{:.6f}".format(dt))             # format the time
    data = (ken.checks, ken.num_assignments, dt)    # get the data
    # print(assignments)
    return assignments, data                    # return the assignments and the data



