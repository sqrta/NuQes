def priority(A, l, m):
    A1, A2, A3 = A[0], A[1], A[2]
    if A1[1] + A2[1] == m:
        return True
    return False
