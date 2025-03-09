from itertools import product
import math
from Solver import Solver

def ALO (lst, solver):
    solver.add_clause(lst)

def AMO_Binomial(lst, solver):
    N = len(lst)
    for i in range(N):
        for j in range(i+1, N):
            solver.add_clause([-lst[i], -lst[j]])

def AMO_Binary(lst, solver, Y):
    # len(Y) = log2(N)
    N = len(lst)

    # Sinh tất cả tổ hợp của Y và -Y
    combinations = list(product(*[(y, -y) for y in Y]))

    # Chỉ lấy số lượng tổ hợp đủ để mã hóa danh sách
    encoding = {lst[i]: combinations[i] for i in range(N)}

    for i in range(N):
        solver.add_clause([-lst[i]] + list(encoding[lst[i]]))

def AMO_SequentialEncounter(lst, solver, S):
    # len(S) = N - 1
    N = len(lst)

    solver.add_clause([-lst[0], S[0]])

    for i in range(1, N - 1):
        solver.add_clause([-lst[i], -S[i-1], S[i]])
        solver.add_clause([-S[i-1], -lst[i]])

    solver.add_clause([-S[N-2], -lst[N-1]])

def AMO_Commander(lst, solver, C):
    N = len(lst)
    M = len(C)
    count = 0
    group_size = math.ceil(N / M)

    AMO_Binomial(C, solver)
    ALO(C, solver)

    for i in range(M):
        group = []
        for j in range(group_size):
            if count < N:
                group.append(lst[count])
                solver.add_clause([C[i], -lst[count]])
                count += 1
        AMO_Binomial(group, solver)
        ALO(group, solver)

def AMO_Product(lst, solver, R, C):
    AMO_Binomial(R, solver)
    AMO_Binomial(C, solver)

    count = 0

    for r in range(len(R)):
        for c in range(len(C)):
            if count < len(lst):
                solver.add_clause([-lst[count], R[r], C[c]])
                count += 1

solver = Solver()
X = [1, 2, 3, 4, 5, 6, 7, 8]
Y = [101, 102, 103]
S = [201, 202, 203, 204, 205, 206, 207]
C = [301, 302, 303, 304]
R = [401, 402]
C = [501, 502, 503, 504]

AMO_Product(X, solver, R, C)

solver.print_clauses()





