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


# ==================================
# Backtracking with Forward Checking
# ==================================
def Backtracking_with_forward_checking(ken, var, value, assignment, removals):
    """Backtracking with Forward Checking Algorithm.

    Args:
        ken (KenKen):  The KenKen instance.
        var (tuple of cells (j, i)):  The variable.
        value (tuple of values):  The value.
        assignment (dict of assignments var : val ):  The assignment.
        removals (list of tuples of cells (j, i) and values):  The removals.

    Returns:
        bool: True iff the chosen value for var doesn't violate the constraints.
    """
    ken.ken_support_current_domains()   # update current_domains
    for B in ken.neighbors[var]:        # for each neighbor of var
        if B not in assignment:         # if B is not in the assignment
            for b in ken.current_domains[B][:]:  # for each value in the current_domains of B
                if not ken.ken_constraints(var, value, B, b):   # if the constraints are not satisfied
                    ken.ken_removals_modify(B, b, removals)     # remove B=b from the current_domains of B
            if not ken.current_domains[B]:                      # if the current_domains of B is empty
                return False            # return False
    return True   # return True iff the chosen value for var doesn't violate the constraints.


def mrv(assignment, csp):
    """Minimum-remaining-values heuristic."""
    return argmin_random_tie(
        [v for v in csp.variables if v not in assignment],
        key=lambda var: num_legal_values(csp, var, assignment))

def num_legal_values(csp, var, assignment):
    if csp.current_domains:
        return len(csp.current_domains[var])
    else:
        return count(csp.ken_nummbers_of_conflicts(var, val, assignment) == 0
                     for val in csp.domains[var])

def lcv(var, assignment, csp):
    """Least-constraining-values heuristic."""
    return sorted(csp.choices(var),
                  key=lambda val: csp.ken_nummbers_of_conflicts(var, val, assignment))