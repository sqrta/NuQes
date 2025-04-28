def priority(A, l, m):
    A1, A2, A3 = A[0], A[1], A[2]
    if A1[0] == "x" and A2[0] == "x" and A3[0] == "y" and A1[1] + A2[1] == l:
        return True
    if A1[0] == "x" and A2[0] == "y" and A3[0] == "y" and A2[1] + A3[1] == m:
        return True
    return False
