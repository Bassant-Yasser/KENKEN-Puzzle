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
 



