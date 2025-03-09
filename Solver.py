class Solver:
    def __init__(self):
        self.clauses = []

    def add_clause(self, clause):
        self.clauses.append(clause)

    def print_clauses(self):
        print("SOLVER:")
        for clause in self.clauses:
            print(clause)
