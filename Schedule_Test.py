from pysat.solvers import Glucose3

A = ["Ngày 1", "Ngày 2", "Ngày 3"]
B = ["Sáng", "Chiều"]
C = ["A", "B", "C", "D", "E"]

def ALO (lst, solver):
    solver.add_clause(lst)

def AMO_Binomial(lst, solver):
    N = len(lst)
    for i in range(N):
        for j in range(i+1, N):
            solver.add_clause([-lst[i], -lst[j]])

def toNum(day, sec, sub):
    return day*100 + sec*10 + sub

def fromNum(num):
    day = num // 100 - 1
    sec = (num // 10) % 10 - 1
    sub = num % 10 - 1
    return [A[day], B[sec], C[sub]]

def print_ans(model):
    for ans in model:
        if ans > 0:
            print(fromNum(ans))

schedule = [[0] * 3 for _ in range(10)]
solver = Glucose3()

for i in range(5):
    for j in range(3):
        schedule[i][j] = toNum(j+1,1,i+1)
        schedule[5+i][j] = toNum(j+1,2,i+1)


# moi mon hoc chi thi 1 lan
for i in range(5):
    ALO(schedule[i] + schedule[5+i], solver)
    AMO_Binomial(schedule[i] + schedule[5+i], solver)

# mot mon hoc khong the thi o hai ca khac nhau trong cung 1 ngay
for i in range(5):
    for j in range(3):
        solver.add_clause([-schedule[i][j], -schedule[5+i][j]])

# A (0) va B (1) khong thi cung ngay
for j in range(3):
    gr = [schedule[0][j], schedule[1][j], schedule[5+0][j], schedule[5+1][j]]
    AMO_Binomial(gr, solver)

# mon C (2) thi vao buoi sang
for j in range(3):
    solver.add_clause([-schedule[5 + 2][j]])

if solver.solve():
        model = solver.get_model()
        print_ans(model)
else:
        print("No answer")