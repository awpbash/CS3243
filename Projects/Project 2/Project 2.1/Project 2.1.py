from typing import List, Dict, Set, Tuple, Any
import heapq

class csp:
    def __init__(self, domain_values, constraint_rules):
        self.domain_values = domain_values
        self.constraint_rules = constraint_rules
        self.variables = list(domain_values.keys())

    #check if assigning a value to a variable is valid
    def is_valid(self, variable, value, current_assignments):
        if variable not in self.constraint_rules:
            return True  #no constraint so valid
        
        for neighbor, constraint_details in self.constraint_rules[variable].items():
            constraint_func, is_forward = constraint_details
            if neighbor in current_assignments:
                if is_forward and not constraint_func(value, current_assignments[neighbor]):
                    return False
                if not is_forward and not constraint_func(current_assignments[neighbor], value):
                    return False
        return True
    
    # Select the next variable to assign based on MRV and Degree heuristics
    def choose_variable(self, current_assignments):
        #compute MRV
        mrv_info = {} #HASHMAP BABEH
        for var in self.domain_values:
            if var not in current_assignments:
                remaining_values = sum(self.is_valid(var, val, current_assignments) for val in self.domain_values[var])
                mrv_info[var] = remaining_values

        #get variables with the fewest remaining values
        min_remaining = min(mrv_info.values())
        candidates = [var for var, count in mrv_info.items() if count == min_remaining]

       
        if len(candidates) == 1:
            return candidates[0]
        
        #if there are multiple variables with the same MRV, apply degree heuristic
        else:
            degree_info = {}
            for var in candidates:
                degree = sum(1 for neighbor in self.constraint_rules[var] if neighbor not in current_assignments)
                degree_info[var] = degree
            return max(degree_info, key=degree_info.get)
        
    # Sort values based on the Least Constraining Value (LCV) heuristic
    def rank_values(self, variable, current_assignments):
        heap = []
        for candidate_value in self.domain_values[variable]:
            temp_assignments = current_assignments.copy()
            temp_assignments[variable] = candidate_value
            lcv_score = 0
            
            for neighbor in self.constraint_rules[variable]:
                if neighbor not in temp_assignments:
                    for neighbor_value in self.domain_values[neighbor]:
                        if self.is_valid(neighbor, neighbor_value, temp_assignments):
                            lcv_score += 1

            #somehow faster than using a list and sort
            heapq.heappush(heap, (-lcv_score, candidate_value))
        # Extract the values from the heap in reverse order of LCV (i.e., most constraining first)
        return [heapq.heappop(heap)[1] for _ in range(len(heap))]
    
    #perform forward checking to reduce the domain of unassigned neighbors
    def forward_check(self, variable, value, current_assignments):
        backup_domain = {}
        for neighbor, constraint_details in self.constraint_rules[variable].items():
            constraint_func, is_forward = constraint_details
            if neighbor not in current_assignments:
                backup_domain[neighbor] = self.domain_values[neighbor]
                pruned_domain = [
                    neighbor_value for neighbor_value in self.domain_values[neighbor]
                    if (is_forward and constraint_func(value, neighbor_value)) or
                    (not is_forward and constraint_func(neighbor_value, value))
                ]
                self.domain_values[neighbor] = pruned_domain

                #if any neighbor's domain becomes empty, forward checking fails
                if not pruned_domain:
                    return False, backup_domain
        return True, backup_domain
    
    #restore the domains after backtracking
    def restore_domains(self, backup_domain):
        for var, domain in backup_domain.items():
            self.domain_values[var] = domain

#prune based on constraints -> reduces intial domain
def prune_invalid_domains(csp):
    for variable in csp.variables:
        if variable not in csp.constraint_rules:
            continue
        valid_values = set()
        for value in csp.domain_values[variable]:
            satisfies_all = True
            for neighbor, constraint_details in csp.constraint_rules[variable].items():
                constraint_func, is_forward = constraint_details
                #use next to check if there is any valid value for the neighbor


                if not next(
                    (True for neighbor_value in csp.domain_values[neighbor]
                     if (is_forward and constraint_func(value, neighbor_value)) or
                     (not is_forward and constraint_func(neighbor_value, value))),
                    False
                ): 
                #over here the next function is used to check if there exist at least 1 True in the generator
                #the generator checks if the value satisfies the constraint with any value in the neighbor's domain
                     
                    satisfies_all = False
                    break  #exit early if any constraint is not satisfied
            
            if satisfies_all:
                valid_values.add(value)
        csp.domain_values[variable] = list(valid_values)
#recursive backtracking function
def backtrack(assignments, csp):
    #all assigned, return assignments
    if len(assignments) == len(csp.variables):
        return assignments
    #choose the next variable to assign
    var_to_assign = csp.choose_variable(assignments)

    #LCV heuristic to rank values
    for value in csp.rank_values(var_to_assign, assignments):
        if csp.is_valid(var_to_assign, value, assignments):
            new_assignments = assignments.copy()
            new_assignments[var_to_assign] = value

            #perform forward checking
            success, backup_domains = csp.forward_check(var_to_assign, value, new_assignments)
            if success:
                result = backtrack(new_assignments, csp)
                if result:
                    return result
            csp.restore_domains(backup_domains)
    return None #no solution found


def solve_CSP(data):
    domains = data["domains"]
    constraints = {}
    for (var1, var2), constraint_func in data["constraints"].items():
        if var1 not in constraints:
            constraints[var1] = {var2: (constraint_func, True)}
        else:
            constraints[var1][var2] = (constraint_func, True)
        if var2 not in constraints:
            constraints[var2] = {var1: (constraint_func, False)}
        else:
            constraints[var2][var1] = (constraint_func, False)
    problem = csp(domains, constraints)
    #pre-process and prune the domains before solving
    prune_invalid_domains(problem)
    return backtrack({}, problem)