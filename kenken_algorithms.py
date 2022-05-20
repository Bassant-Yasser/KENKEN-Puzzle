from time           import time
from kenken_helper  import *
from utils          import *


# algorithms_Fn = {
#     "BT":           lambda ken: backtracking_search(ken, assignment={}),
#     "BT+FC":        lambda ken: backtracking_search(ken, assignment={}, inference=Backtracking_with_forward_checking),
#     "BT+MAC":       lambda ken: backtracking_search(ken, assignment={}, inference=Maintain_arc_consistency)
# }   # algorithms_Fn dict for algorithms names and functions

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

    def ken_constraints(self, A, a, B, b):
        """ Return True iff A is B or A is not conflicting with B.
        Args:
            A (tuple of cells (j, i)):  The first set of cells.
            a (tuple of values):  The first values.
            B (tuple of cells (j, i)):  The second set of cells.
            b (tuple of values):  The second values.

        Returns:
            bool: True iff A and B are conflicting.
        """
        self.checks += 1        # increment the number of checks
        # return True iff A and B are conflicting
        return A == B or not conflicting(A, a, B, b)    

      
    def ken_increase_assignment(self, var, val, assignment):
        """Increment the number of assignments.
        Args:
            var (tuple of cells (j, i)):  The variable.
            val (tuple of values):  The value.
            assignment (dict of assignments var : val ):  The assignment.
        """
        assignment[var] = val               # add the assignment to the assignment dict
        self.num_assignments += 1           # increment the number of assignments

    def ken_unassignment(self, var, assignment):
        """Remove var from assignment.

        Args:
            var (tuple of cells (j, i)):  The variable.
            assignment (dict of assignments var : val ):  The assignment.
        """
        if var in assignment:                # if the variable is in the assignment
            del assignment[var]              # remove the variable from the assignment

    def ken_nummbers_of_conflicts(self,var , val , assignments):
        """Return the number of conflicts for var=val.
        Args:
            var (tuple of cells (j, i)):  The variable.
            val (tuple of values):  The value.
            assignments (dict of assignments var : val ):  The assignment.
        Returns:
            int: The number of conflicts.
        """
        conflicts = 0                       # number of conflicts
        for c in self.neighbors[var]:       # for each neighbor of var
            # if the neighbor is in the assignment and the constraint is not satisfied
            if c in assignments and not self.ken_constraints(var, val, c, assignments[c]): 
                conflicts += 1              # increment the number of conflicts
        return conflicts                    # return the number of conflicts
 
    def ken_support_current_domains(self):
        """Update current_domains to reflect the current domains of the variables."""
        if self.current_domains is None:    # if current_domains is None
            self.current_domains= {}        # create a new current_domains
            for v in self.variables:            # for each variable
                # add the domain to the current_domains
                self.current_domains[v] = list(self.domains[v]) 
        
    def ken_assumption_of_removals(self, var, value):
        """Return the removals for var=value.

        Args:
            var (tuple of cells (j, i)):  The variable.
            value (tuple of values):  The value.

        Returns:
            list of tuples of cells (j, i) and values:  The removals.  
        """
        self.ken_support_current_domains()  # update current_domains
        removals = []                       # list of removals
        for it in self.current_domains[var]:    # for each value in the current_domains
            if it != value:                     # if the value is not the value we are looking for
                removals.append((var, it))      # add the value to the list of removals
        self.current_domains[var] = [value]     # update the current_domains
        return removals            # return the list of removals


    def ken_removals_modify(self, var, value, removals):
        """Remove var=value from the current domains of the variables.

        Args:
            var (tuple of cells (j, i)):  The variable.
            value (tuple of values):  The value.
            removals (list of tuples of cells (j, i) and values):  The removals.
        """
        self.current_domains[var].remove(value)     # remove the value from the current_domains
        if removals is not None:                    # if the removals is not None
            removals.append((var, value))           # add the value to the removals

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

    def ken_restore(self, removals):
        """Restore the current domains of the variables.

        Args:
            removals (list of tuples of cells (j, i) and values):  The removals.
        """
        # for each removal in the removals
        for B, b in removals:          
            # add the value to the current_domains
            self.current_domains[B].append(b)   

class solver:
    def __init__(self, size, Groups):
        self.ken = Kenken(size, Groups)
    # ==============================================================================
    # Inference Algorithms
    # ===============================================================================
    # ==================================
    # Maintain arc consistency.
    # ==================================

    def successful_removal(self, Xi, Xj, removals):
        """Return True iff the removal of Xi from Xj was successful.

        Args:
            ken (KenKen):  The KenKen instance.
            Xi (tuple of cells (j, i)):  The first variable.
            Xj (tuple of cells (j, i)):  The second variable.
            removals (list of tuples of cells (j, i) and values):  The removals.

        Returns:
            bool: True iff the removal of Xi from Xj was successful.
        """
        suc_removal = False                         # successful removal
        for x in self.ken.current_domains[Xi][:]:        # for each value in the current_domains of Xi
            # if all the constraints are satisfied
            if all(not self.ken.ken_constraints(Xi, x, Xj, y) for y in self.ken.current_domains[Xj]):     
                self.ken.ken_removals_modify(Xi, x, removals)        # remove Xi=x from the current_domains of Xi
                suc_removal = True               # successful removal
        return suc_removal                       # return the successful removal

    def Maintain_arc_consistency(self, var, value, assignment, removals):
        """Maintain arc consistency Algorithm.

        Args:
            ken (KenKen):  The KenKen instance.
            var (tuple of cells (j, i)):  The variable.
            value (tuple of values):  The value.
            assignment  (dict of assignments var : val ):  The assignment.
            removals (list of tuples of cells (j, i) and values):  The removals.

        Returns:
            bool: True iff the Algorithm was successful to maintain arc consistency.
        """
        Arc = []                 # arcs queue
        for X in self.ken.neighbors[var]:    # for each neighbor of var
            Arc.append((X, var))        # add the arc to the queue
        self.ken.ken_support_current_domains()   # update current_domains
        while Arc:           # while the queue is not empty
            (Xi, Xj) = Arc.pop()    # remove the arc from the queue
            if self.successful_removal( Xi, Xj, removals):   # if the removal was successful
                if not self.ken.current_domains[Xi]:             # if the current_domains of Xi is empty
                    return False           # return False
                for Xk in self.ken.neighbors[Xi]:                # for each neighbor of Xi
                    if Xk != Xj:                            # if Xk is not Xj
                        Arc.append((Xk, Xi))                # add the arc to the queue
        return True     # return True iff the Algorithm was successful to maintain arc consistency
        

    # ==================================
    # Backtracking with Forward Checking
    # ==================================
    def Backtracking_with_forward_checking(self, var, value, assignment, removals):
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
        self.ken.ken_support_current_domains()   # update current_domains
        for B in self.ken.neighbors[var]:        # for each neighbor of var
            if B not in assignment:         # if B is not in the assignment
                for b in self.ken.current_domains[B][:]:  # for each value in the current_domains of B
                    if not self.ken.ken_constraints(var, value, B, b):   # if the constraints are not satisfied
                        self.ken.ken_removals_modify(B, b, removals)     # remove B=b from the current_domains of B
                if not self.ken.current_domains[B]:                      # if the current_domains of B is empty
                    return False            # return False
        return True   # return True iff the chosen value for var doesn't violate the constraints.

    def mrv(self,assignment):
        """Minimum-remaining-values heuristic."""
        return argmin_random_tie(
            [v for v in self.ken.variables if v not in assignment],
            key=lambda var: self.num_legal_values(var, assignment))

    def num_legal_values(self, var, assignment):
        if self.ken.current_domains:
            return len(self.ken.current_domains[var])
        else:
            return count(self.ken.ken_nummbers_of_conflicts(var, val, assignment) == 0
                        for val in self.ken.domains[var])

    def lcv(self, var, assignment):
        """Least-constraining-values heuristic."""
        return sorted(self.ken.choices(var),
                    key=lambda val: self.ken.ken_nummbers_of_conflicts(var, val, assignment))
    # ==========================================================
    # Backtracking Algorithm for solving the KenKen puzzle.
    # ==========================================================
    default_inference = lambda self, var, value, assignment, removals: True  # default inference returns True

    def backtracking_search(self,
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
        if len(assignment) == len(self.ken.variables):   # if the assignment is complete
            return assignment                       # return the assignment
        # select first unassigned variable
        var =first(list(set(self.ken.variables)-assignment.keys())) # mrv(assignment,ken)
        for value in self.ken.ken_choose_domain(var):    # for each value in the domain of var  #lcv(var,assignment, ken):#
            if self.ken.ken_nummbers_of_conflicts(var, value, assignment) == 0:  # if there is no conflict
                self.ken.ken_increase_assignment(var, value, assignment)         # increase the assignment
                removals = self.ken.ken_assumption_of_removals(var, value)       # get the removals
                if inference( var, value, assignment, removals):        # if the inference is successful
                    result = self.backtracking_search(assignment,inference)  # recursive call to the backtracking_search
                    if result is not None:                             # if the result is not None
                        return result                                  # return the result
                self.ken.ken_restore(removals)                              # restore the removals
                self.ken.ken_unassignment(var, assignment)                  # unassign the variable
        return None    # return None if the assignment is not complete
    def solve(self, Algorithm_name):
        if Algorithm_name == "BT":
            return self.backtracking_search(assignment={}, inference=self.default_inference)
        elif Algorithm_name == "BT+FC":
            return self.backtracking_search(assignment={}, inference=self.Backtracking_with_forward_checking)
        elif Algorithm_name == "BT+MAC":
            return self.backtracking_search(assignment={}, inference=self.Maintain_arc_consistency)
        return None


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

    # selected_algorithm = algorithms_Fn[name]    # get the algorithm  
    # ken = Kenken(size, groups_puzzle)           # create the KenKen instance
    ahmed = solver(size,groups_puzzle)

    dt = time()                                 # get the current time
    # assignments = selected_algorithm(ken)       # get the assignments
    assignments = ahmed.solve(name)
    dt = time() - dt                            # get the time difference
    dt = float("{:.6f}".format(dt))             # format the time
    data = (ahmed.ken.checks, ahmed.ken.num_assignments, dt)    # get the data
    # print(assignments)
    return assignments, data                    # return the assignments and the data
