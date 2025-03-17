from itertools import product, combinations
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

def AMK_Naive(lst, solver, k):
    # ALO (k+1) false:

    for sub in combinations(lst, k+1):
        solver.add_clause([-var for var in sub])

def ALK_Naive(lst, solver, k):

    # ALO (n-k+1) true:
    for sub in combinations(lst, len(lst) - k + 1):
        solver.add_clause([var for var in sub])

def EK_Naive(lst, solver, k):
    AMK_Naive(lst, solver, k)
    ALK_Naive(lst, solver, k)

def EK_NewSequentialCounter(lst, solver, k, R):
    n = len(lst) - 1

    # R[n-1][k]: ma tran co n-1 dong va k cot
    # Rij: i - X1 -> Xi; j - co dung j <= k gia tri true
    # (1) Xi -> Ri,1
    for i in range(n):
        solver.add_clause([-lst[i], R[i][0]])

    # (2) Ri-1,j -> Ri,j
    for i in range(1, n):
        for j in range(min(i,k)):
            solver.add_clause([-R[i-1][j], R[i][j]])

    # (3) Xi and Ri-1,j-1 -> Ri,j
    for i in range(1,n):
        for j in range(1,min(i,k)):
            solver.add_clause([-lst[i], -R[i-1][j-1], R[i][j]])

    # (4) notXi and notRi-1,j -> notRi,j
    for i in range(1, n):
        for j in range(min(i,k)):
            solver.add_clause([lst[i], R[i-1][j], -R[i][j]])

    # (5) notXi -> notRi,i
    for i in range(k):
        solver.add_clause([lst[i], -R[i][i]])

    # (6) notRi-1,j-1 -> not Ri,j
    for i in range(1,n):
        for j in range(1,min(i,k)):
            solver.add_clause([R[i-1][j-1], -R[i][j]])

    return

def ALK_NewSequentialCounter(lst, solver, k, R):
    # (1) -> (6):
    EK_NewSequentialCounter(lst, solver, k, R)

    n = len(lst) - 1
    # (7) Rn-1,k or (Xn and Rn-1,k-1)

    solver.add_clause([R[n-1][k-1], lst[n]])
    solver.add_clause([R[n-1][k-1], R[n-1][k-2]])

def AMK_NewSequentialCounter(lst, solver, k, R):
    n = len(lst) - 1

    # R[n-1][k]: ma tran co n-1 dong va k cot
    # Rij: i - X1 -> Xi; j - co dung j <= k gia tri true
    # (1) Xi -> Ri,1
    for i in range(n):
        solver.add_clause([-lst[i], R[i][0]])

    # (2) Ri-1,j -> Ri,j
    for i in range(1, n):
        for j in range(min(i, k)):
            solver.add_clause([-R[i - 1][j], R[i][j]])

    # (3) Xi and Ri-1,j-1 -> Ri,j
    for i in range(1, n):
        for j in range(1, min(i, k)):
            solver.add_clause([-lst[i], -R[i - 1][j - 1], R[i][j]])

    # (8) xi -> notRi-1,k

    for i in range(k, n+1):
        solver.add_clause([-lst[i], -R[i-1][k-1]])





