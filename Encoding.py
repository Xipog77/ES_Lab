from itertools import product, combinations
import math
from Solver import Solver

def ALO (lst: list[int], solver):
    solver.add_clause(lst)

def AMO_Binomial(lst: list[int], solver):
    N = len(lst)
    for i in range(N):
        for j in range(i+1, N):
            solver.add_clause([-lst[i], -lst[j]])

def AMO_Binary(lst: list[int], solver, Y):
    # len(Y) = log2(N)
    N = len(lst)

    # Sinh tất cả tổ hợp của Y và -Y
    combinations = list(product(*[(y, -y) for y in Y]))

    # Chỉ lấy số lượng tổ hợp đủ để mã hóa danh sách
    encoding = {lst[i]: combinations[i] for i in range(N)}

    for i in range(N):
        solver.add_clause([-lst[i]] + list(encoding[lst[i]]))

def AMO_SequentialEncounter(lst: list[int], solver, S):
    # len(S) = N - 1
    N = len(lst)

    solver.add_clause([-lst[0], S[0]])

    for i in range(1, N - 1):
        solver.add_clause([-lst[i], -S[i-1], S[i]])
        solver.add_clause([-S[i-1], -lst[i]])

    solver.add_clause([-S[N-2], -lst[N-1]])

def AMO_Commander(lst: list[int], solver, C):
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

def AMO_Product(lst: list[int], solver, R, C):
    AMO_Binomial(R, solver)
    AMO_Binomial(C, solver)

    count = 0

    for r in range(len(R)):
        for c in range(len(C)):
            if count < len(lst):
                solver.add_clause([-lst[count], R[r], C[c]])
                count += 1

def AMK_Naive(lst: list[int], solver, k):
    # ALO (k+1) false:

    for sub in combinations(lst, k+1):
        solver.add_clause([-var for var in sub])

def ALK_Naive(lst: list[int], solver, k):

    # ALO (n-k+1) true:
    for sub in combinations(lst, len(lst) - k + 1):
        solver.add_clause([var for var in sub])

def EK_Naive(lst: list[int], solver, k):
    AMK_Naive(lst, solver, k)
    ALK_Naive(lst, solver, k)

def EK_NewSequentialCounter(lst : list[int], solver, k, R):
    n = len(lst) - 1

    # R[n][k + 1]: ma tran co n dong va k + 1 cot
    # Rij: i - X1 -> Xi; j - co dung j <= k gia tri true
    # (1) Xi -> Ri,1
    for i in range(1, n):
        solver.add_clause([-lst[i], R[i][1]])

    # (2) Ri-1,j -> Ri,j
    for i in range(2, n):
        for j in range(1, min(i - 1,k) + 1):
            solver.add_clause([-R[i-1][j], R[i][j]])

    # (3) Xi and Ri-1,j-1 -> Ri,j
    for i in range(2,n):
        for j in range(2,min(i,k) + 1):
            solver.add_clause([-lst[i], -R[i-1][j-1], R[i][j]])

    # (4) notXi and notRi-1,j -> notRi,j
    for i in range(2, n):
        for j in range(1, min(i - 1,k) + 1):
            solver.add_clause([lst[i], R[i-1][j], -R[i][j]])

    # (5) notXi -> notRi,i
    for i in range(1, k + 1):
        solver.add_clause([lst[i], -R[i][i]])

    # (6) notRi-1,j-1 -> not Ri,j
    for i in range(2,n):
        for j in range(2,min(i,k) + 1):
            solver.add_clause([R[i-1][j-1], -R[i][j]])

    return

def ALK_NewSequentialCounter(lst: list[int], solver, k, R):
    # (1) -> (6):
    EK_NewSequentialCounter(lst, solver, k, R)

    n = len(lst) - 1
    # (7) Rn-1,k or (Xn and Rn-1,k-1)

    solver.add_clause([R[n-1][k], lst[n]])
    solver.add_clause([R[n-1][k], R[n-1][k-1]])

def AMK_NewSequentialCounter(lst: list[int], solver, k, R):
    n = len(lst) - 1

    # R[n-1][k]: ma tran co n-1 dong va k cot
    # Rij: i - X1 -> Xi; j - co dung j <= k gia tri true

    # (8) xi -> notRi-1,k

    for i in range(k + 1, n+1):
        solver.add_clause([-lst[i], -R[i-1][k]])

def EK_NewSequentialCounter_Shorten(lst: list[int], solver, k, n):
    global id_variable
    x = len(lst) - 1
    assert x == k * n
    map_register = [[0 for j in range(k + 1)] for i in range(x + 1)]

    for id in range(1, n + 1):
        L =  (id - 1) * k
        for i in range(L + 1, L + k + 1):
            for j in range(1, i - L + 1):
                id_variable += 1
                map_register[i][j] = id_variable

        # (1): If a bit is true, the first bit of the corresponding register is true
        for i in range(L + 1, L + k + 1):
            solver.add_clause([lst[i], -map_register[i][i - L]])
            solver.add_clause([-lst[i], map_register[i][1]])

        # (2): If R[i - 1][j] = 1, R[i][j] = 1;
        for i in range(L + 2, L + k + 1):
            for j in range(1, i - L):
                solver.add_clause([lst[i], map_register[i - 1][j], -map_register[i][j]])
                solver.add_clause([-map_register[i - 1][j], map_register[i][j]])

        # (3): If bit i is on and R[i - 1][j - 1] = 1, R[i][j] = 1;
        for i in range(L + 2, L + k + 1):
            for j in range(2, i - L + 1):
                solver.add_clause([-lst[i], -map_register[i - 1][j - 1], map_register[i][j]])
                solver.add_clause([map_register[i - 1][j - 1], -map_register[i][j]])

    bonus = [[0 for j in range(k + 1)] for i in range(n - 1)]
    for id in range(n - 1):
        for i in range(1, k + 1):
            id_variable += 1
            bonus[id][i] = id_variable

        a = map_register[(id + 2) * k]
        b = []
        if id == 0: b = map_register[k]
        else: b = bonus[id - 1]

        for i in range(1, k + 1):
            solver.add_clause([-a[i], bonus[id][i]])
            solver.add_clause([-b[i], bonus[id][i]])
            for j in range(1, k + 1):
                if i + j <= k: solver.add_clause([-a[i], -b[j], bonus[id][i + j]])
                if i + j - 1 <= k: solver.add_clause([a[i], b[j], -bonus[id][i + j - 1]])
                if i + j == k + 1: solver.add_clause([-a[i], -b[j]])

    solver.add_clause([bonus[n - 2][k]])

def AMO_StaireCase(lst: list[int], solver, R, w):
    #w: width: so nhom
    #R[n//w][w]
    n = len(lst)
    groups = (n + w - 1) // w

    # (1) (X_i → R_{g,1})
    for i in range(n):
        group = i // w
        solver.add_clause([-lst[i], R[group][i%w]])

    # (2) (R_{g,j} → R_{g,j+1})
    for group in range(groups):
        for j in range(w - 1):
            solver.add_clause([-R[group][j], R[group][j + 1]])

    # (3) (X_i → R_{g,j-1} ∨ ¬R_{g,j})
    for i in range(n):
        group = i // w
        for j in range(1, w):
            solver.add_clause([lst[i], R[group][j-1], -R[group][j]])

    # (4) (¬R_{g,j} ∨ ¬R_{g,j+1})
    for group in range(groups):
        for j in range(w - 1):
            solver.add_clause([-R[group][j], -R[group][j + 1]])









