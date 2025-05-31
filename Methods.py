import random
from Functions import literal_set
from collections import Counter


def literal_choice(clauses, method):
    '''

   Function that selects a literal based on the chosen method. The method must be one of the options below:
   "first_literal" - Selects the first literal found in the first clause
   "random_literal" - Randomly selects a literal from the set of all literals in the formula
   "most_frequent_literal" - Chooses the literal that appears most frequently (positive or negative) in all clauses
   "dlis" - Counts occurrences of each literal and its negation, then chooses the literal with the highest combined count
   "jeroslow_wang" - Picks the literal with the highest score, computed by a specific formula
   "moms" - Finds the shortest clauses and chooses the literal that appears most within those
    '''
    if method == "first_literal":
        return next(iter(next(iter(clauses))))

    if method == "random_literal":
        return random.choice(list(literal_set(clauses)))

    if method == "most_frequent_literal":
        counter = Counter(lit for clause in clauses for lit in clause)
        return max(counter, key=counter.get)

    if method =="dlis":
        literals=literal_set(clauses)
        occurrence_count = {literal: 0 for literal in literals}
        for clause in clauses:
            for literal in clause:
                if literal in literals:
                    occurrence_count[literal] += 1
                if -literal in literals:
                    occurrence_count[-literal] += 1
        best_literal = None
        max_occurrence = -1
        for literal, count in occurrence_count.items():
            if count > max_occurrence:
                best_literal = literal
                max_occurrence = count

        return best_literal


    if method == "jeroslow_wang":
        scores = Counter()
        for clause in clauses:
            weight = 2 ** -len(clause)
            for lit in clause:
                scores[lit] += weight
        return max(scores, key=scores.get) if scores else None

    if method == "moms":
        literals=literal_set(clauses)
        if not clauses or not literals:
            return None

        min_size = min(len(clause) for clause in clauses if clause)
        min_clauses = [clause for clause in clauses if len(clause) == min_size]

        literal_counts = {}
        for clause in min_clauses:
            for lit in clause:
                var = abs(lit)
                if var in literals:
                    literal_counts[lit] = literal_counts.get(lit, 0) + 1
        if not literal_counts:
            return None
        best_literal = max(literal_counts, key=literal_counts.get)
        return best_literal




