from Functions import *
from Methods import *
import time

def resolution_solver(clauses, p=False):
    '''
    Solves the SAT problem using the resolution algorithm.
    It iteratively applies the resolution rule to pairs
    of clauses until either a contradiction (empty clause) is
    found or no new resolvents can be added.
    '''
    clauses = [frozenset(clause) for clause in clauses]
    idx = 1

    for clause in clauses:
        if p: print(f"{idx}: {set(clause)}")
        idx += 1

    while True:
        new_clause_set = set()
        clause_set = set(clauses)
        if not clauses:
            print("SATISFIABLE")
            return True
        clause_pairs = []
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                clause_pairs.append((clauses[i], clauses[j]))
        for (ci, cj) in clause_pairs:
            resolvents = resolve(ci, cj)
            for resolvent in resolvents:
                resolvent = frozenset(resolvent)
                if not resolvent:
                    if p:
                        print(f"({idx}) {{}} from {set(ci)} and {set(cj)}")
                    print("UNSATISFIABLE")
                    return False
                if resolvent not in clause_set and resolvent not in new_clause_set:
                    if p: print(f"{idx}: {set(resolvent)} from {set(ci)} and {set(cj)}")
                    new_clause_set.add(resolvent)
                    idx += 1
        if not new_clause_set:
            if p:
                print("\nNo new resolvent can be added")
            print("SATISFIABLE")
            return True
        clauses.extend(new_clause_set)


def dp_solver(clauses, p=False):
    """
    DP solver that interleaves simplification rules with
    limited resolution steps to generate new clauses only
    as needed, then returns to simplification.
    """
    clauses = [frozenset(c) for c in clauses]
    while True:
        clauses = apply_simplifications(clauses)

        if clauses == {frozenset()}:
            print("UNSATISFIABLE")
            return False
        if not clauses:
            print("SATISFIABLE")
            return True

        if p:
            print("No simplification applicable, applying one step of resolution")

        clauses, added_new = limited_resolution_step(clauses, p)

        if clauses == {frozenset()}:
            return False  # UNSAT found during resolution

        if not added_new:
            if p:
                print("No new clauses from resolution, problem SAT")
            print("SATISFIABLE")
            return True



def dpll(clauses, s, splitting_method,splits=0, p=False):
    '''
    Core recursive function of the DPLL algorithm,
    it simplifies the clause set using unit clause and pure literal rules,
    then recursively splits on a chosen literal using a given splitting_method
    '''
    print_clause_set(clauses, p)
    clauses = unit_clause_rule(clauses, p)
    e = {frozenset()}

    if e in clauses or clauses == e:
        if p: print(f"Empty clause found, UNSATISFIABLE")
        return False, splits

    elif not clauses:
        if p: print(f"Empty clause set, SATISFIABLE")
        return True, splits


    clauses = pure_literal_rule(clauses, p)
    if not clauses:
        if p: print(f"SATISFIABLE")
        return True, splits

    if p: print(f"No more unit clause or pure literal rules, choosing a literal to branch on")
    s += 1


    l = literal_choice(clauses, splitting_method)
    if p: print(f"Adding literal {l} to positive clause set")
    splits += 1
    new_clauses_pos = clauses.copy()
    new_clauses_pos.add(frozenset({l}))
    print_clause_set(new_clauses_pos, p)

    if p: print(f"Recursively calling DPLL with positive branch for literal {l}")
    result, splits = dpll(new_clauses_pos, s,splitting_method, splits, p)
    if result:
        return True, splits


    if p: print(f"Adding literal {l}, to negative clause set")
    new_clauses_neg = clauses.copy()
    new_clauses_neg.add(frozenset({-l}))
    print_clause_set(new_clauses_neg, p)

    if p: print(f"Recursively calling DPLL with negative branch for literal {-l}")
    return dpll(new_clauses_neg, s,splitting_method, splits, p)



def dpll_solver(clauses, splitting_method,p=False):
    '''
 Function that starts the DPLL solving process using the given splitting_method.
 IT prints whether the formula is satisfiable and the number of splits performed
 if verbose mode is on (p is set to True).
    '''
    s = 0
    if p: print("Starting DPLL Solver:")
    result, splits = dpll(clauses, s,splitting_method, 0, p=p)
    if result:
        print("SATISFIABLE")
    else:
        print("UNSATISFIABLE")
    if p: print(f"Number of splits: {splits}")

####### Function for measuring time performance of solvers ###########
def resolution_time(clauses, file_name):
    print("---Resolution---")
    start_time = time.perf_counter()
    resolution_solver(clauses, p=False)
    resolution_solver_time = time.perf_counter() - start_time
    log_results("Resolution", file_name, resolution_solver_time)

def dp_time(clauses, file_name):
    print("---DP---")
    start_time = time.perf_counter()
    dp_solver(clauses, p=False)
    dp_solver_time = time.perf_counter() - start_time
    log_results("DP", file_name, dp_solver_time)

def dpll_time(clauses, file_name, splitting_method):
    print(f"---DPLL {splitting_method}---")
    start_time = time.perf_counter()
    dpll_solver(clauses, splitting_method, p=False)
    dpll_solver_time = time.perf_counter() - start_time
    log_results(f"DPLL {splitting_method}", file_name, dpll_solver_time)


#####Splitting methods for DPLL#####
splitting_methods = [
    "first_literal",
    "random_literal",
    "most_frequent_literal",
    "dlis",
    "jeroslow_wang",
    "moms"
]

###### MAIN #######
file_name = "test cases/Small Tests/C1.5.txt"
clauses = load_from_file(file_name)

resolution_time(clauses, file_name)
dp_time(clauses, file_name)

for splitting_method in splitting_methods:
    dpll_time(clauses, file_name, splitting_method)