####### Function for printing clause set ########
def print_clause_set(clauses, p=False):
    idx = 1
    for clause in clauses:
        if p:
            if clause:
                print(f"{idx}: {set(clause)}")
            else:
                print("EMPTY SET")
            idx += 1
######Function to write results in file########
def log_results(algorithm_name, file_name, elapsed_time):
    try:
        with open("test_results.txt", "a") as log_file:
            log_file.write(f" {algorithm_name},  {file_name}, {elapsed_time:.6f} seconds\n")
            log_file.write("------------\n")  # Add the line of dashes
    except Exception as e:
        print(f"Error writing to file: {e}")



####### Function for reading from file ########
def load_from_file(filename):
    clauses = set()
    with open(filename, 'r') as f:
        for line in f:
            literals = {int(x) for x in line.strip().split() if x != '0'}
            if literals:
                clauses.add(frozenset(literals))
    return clauses


######## Function for set of literals #######
def literal_set(clauses):
    literals = set()
    for clause in clauses:
        literals.update(clause)  # Add all elements from each frozenset
    return literals


######Functions for RESOLUTION #######
def resolve(ci, cj):
    '''
    Function which attempts to resolve two clauses ci and cj
    by eliminating the pair of complementary literals.
    It returns a list of resolvent clauses that are not tautologies.
    '''
    resolvents = []
    for lit in ci:
        if -lit in cj:
            resolvent = (ci - {lit}) | (cj - {-lit})
            if not is_tautology(resolvent):
                resolvents.append(resolvent)
    return resolvents

def is_tautology(clause):
    return any(-lit in clause for lit in clause)


######Functions for DP and DPLL #######
def is_unit_clause(clause):
    '''
    Function which returns True if given clause only contains one literal (is a unit clause)
    '''
    return len(clause) == 1

def find_unit_clauses(clauses):
    '''
    Fucntion which identifies all unit clauses in a set of clauses.
    '''
    return {next(iter(c)) for c in clauses if is_unit_clause(c)}

def unit_clause_rule(clauses, p=False):
    '''
    Function which applies the unit clause rule repeatedly:
    assigns values to satisfy unit clauses and simplifies the remaining formula accordingly.
    If a contradiction is found, the function returns an empty clause.
    '''
    while True:
        unit_literals = find_unit_clauses(clauses)
        if not unit_literals:
            break
        for lit in unit_literals:
            if clauses and clauses != {frozenset()}:
                if p: print(f"Applying unit clause rule with literal {lit}")
                clauses = {c for c in clauses if lit not in c}
                neg_literal = -lit
                new_clauses = set()
                for clause in clauses:
                    if neg_literal in clause:
                        new_clause = frozenset(l for l in clause if l != neg_literal)
                        if not new_clause:
                            return {frozenset()}
                        new_clauses.add(new_clause)
                    else:
                        new_clauses.add(clause)
                clauses = new_clauses
                print_clause_set(clauses, p)

    return clauses


def find_pure_literals(clauses):
    '''

    Function which returns all pure literals in the clause set (literals that appear with only one polarity, either positive or negative)
    '''
    literals = set()
    for clause in clauses:
        literals.update(clause)
    pure_literals = {lit for lit in literals if -lit not in literals}
    return pure_literals


def pure_literal_rule(clauses, p=False):
    '''

    Function which applies the pure literal rule iteratively:
    removes all clauses containing pure literals.
    '''
    while True:
        if not clauses:
            return clauses
        pure_literals = find_pure_literals(clauses)
        if not pure_literals:
            break
        for lit in pure_literals:
            if clauses == {frozenset()}:
                return clauses
            if p: print(f"Applying pure literal rule for literal {lit}")
            clauses = {clause for clause in clauses if lit not in clause}
            print_clause_set(clauses, p)
            if not clauses:
                return clauses
    return clauses



def apply_simplifications(clauses):
        prev_len = None
        while prev_len != len(clauses):
            prev_len = len(clauses)
            clauses = unit_clause_rule(clauses, p=False)
            if clauses == {frozenset()}:
                return clauses
            clauses = pure_literal_rule(clauses, p=False)
            if clauses == {frozenset()}:
                return clauses
        return clauses


def limited_resolution_step(clauses, p=False):
    """
    Applies one round of resolution over clause pairs,
    adding any new resolvents found.
    Stops after one pass.
    Returns (new_clauses, added_new_clause: bool)
    """
    clauses = [frozenset(c) for c in clauses]
    clause_set = set(clauses)
    new_clause_set = set()

    clause_pairs = []
    for i in range(len(clauses)):
        for j in range(i + 1, len(clauses)):
            clause_pairs.append((clauses[i], clauses[j]))

    idx = len(clauses) + 1
    for (ci, cj) in clause_pairs:
        resolvents = resolve(ci, cj)
        for resolvent in resolvents:
            resolvent = frozenset(resolvent)
            if not resolvent:
                if p:
                    print(f"({idx}) {{}} from {set(ci)} and {set(cj)}")
                print("UNSATISFIABLE")
                return {frozenset()}, True  # Empty clause found = conflict
            if resolvent not in clause_set and resolvent not in new_clause_set:
                if p:
                    print(f"{idx}: {set(resolvent)} from {set(ci)} and {set(cj)}")
                new_clause_set.add(resolvent)
                idx += 1

    if not new_clause_set:
        return clauses, False
    else:
        return list(clause_set.union(new_clause_set)), True