from pysat.solvers import Glucose3

N = int(input("Kich thuoc ban co:"))

def toNum(row, col):
    return row * N + col + 1

def fromNum(num):
    row = (num - 1) // N
    col = (num - 1) % N
    return row, col

def print_ans(model):
    board = [['-'] * N for _ in range(N)]

    for ans in model:
        if ans > 0:
            row, col = fromNum(ans)
            board[row][col] = 'Q'

    for row in board:
        print(" ".join(row))

def Nqueens_solve():
    chess = [[toNum(r, c) for c in range(N)] for r in range(N)]

    solver = Glucose3()
    # EXO in row
    for r in range(N):
        # ALO in row
        solver.add_clause(chess[r])
        for c in range(N):
            for k in range(c + 1, N):
                # AMO in row
                solver.add_clause([-chess[r][c], -chess[r][k]])
    # EXO in col
    for c in range(N):
        # ALO in col
        col = [chess[i][c] for i in range(N)]
        solver.add_clause(col)
        for r in range(N):
            for k in range(r + 1, N):
                # AMO in row
                solver.add_clause([-chess[r][c], -chess[k][c]])

    # AMO in dia
    for r1 in range(N):
        for r2 in range(N):
            for c1 in range(N):
                for c2 in range(N):
                    if (r1 != r2 and c1 != c2) and (abs(r1 - r2) == abs(c1 - c2)):
                        solver.add_clause([-chess[r1][c1], -chess[r2][c2]])

    if solver.solve():
        model = solver.get_model()
        print_ans(model)
    else:
        print("No answer")

Nqueens_solve()

