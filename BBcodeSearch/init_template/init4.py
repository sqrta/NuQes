def priority(A, l, m):
    A1, A2, A3 = A[0], A[1], A[2]
    if (A3[1] + A2[1]) % l == 0:
        return True
    return False
