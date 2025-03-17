from pysat.solvers import Glucose3
import Encoding
from ES_Lab.Encoding import EK_NewSequentialCounter

solver1 = Glucose3()
solver2 = Glucose3()

X1 = 1
X2 = 2
X3 = 3
X4 = 4
X5 = 5

R11 = 6
R21 = 7
R22 = 8
R31 = 9
R32 = 10
R41 = 11
R42 = 12

lst = [100, 200, 300, 400, 500]
R =[[600],[700, 800],[900, 1000],[1100, 1200]]

# (1)
clauses1 = [[-X1, R11], [-X2, R21], [-X3, R31], [-X4, R41]]
for clause in clauses1:
    solver1.add_clause(clause)

# (2)
clauses2 = [[-R11, R21], [-R21, R31], [-R22, R32], [-R31, R41], [-R32, R42]]
for clause in clauses2:
    solver1.add_clause(clause)

# (3)
clauses3 = [[-X2, -R11, R22], [-X3, -R21, R32], [-X4, -R31, R42]]
for clause in clauses3:
    solver1.add_clause(clause)

# (4)
clauses4 = [[X2, R11, -R21], [X3, R21, -R31], [X3, R22, -R32], [X4, R31, -R41], [X4, R32, -R42]]
for clause in clauses4:
    solver1.add_clause(clause)

# (5)
clauses5 = [[X1, -R11], [X2, R22]]
for clause in clauses5:
    solver1.add_clause(clause)

# (6)
clauses6 = [[R11, -R22], [R21, -R32], [R31, -R42]]
for clause in clauses6:
    solver1.add_clause(clause)

if solver1.solve():
    model = solver1.get_model()
    for ans in model:
        if ans > 0:
            print(ans)
else:
    print("No answer")

EK_NewSequentialCounter(lst, solver2, 2, R)
if solver2.solve():
    model = solver2.get_model()
    for ans in model:
        if ans > 0:
            print(ans)
else:
    print("No answer")





