
def funcScore():
    score = 0
    for key in allCodes.keys():
        l, m = key
        best = 0
        for code in allCodes[key]:
            if priority(code["A"], l, m):
                r = code["k"] * code["d"] / code["n"]
                if r > best:
                    best = r
        score += best
    return score


def priority(A, l, m):
    """Improved version of `priority_v1`."""
    A1, A2, A3 = A[0], A[1], A[2]
    if A1[1] + A2[1] == m or A2[1] + A3[1] == m:
        return True
    if A1[0] == "x" and A2[0] == "x" and A3[0] == "y" and A1[1] + A2[1] == l:
        return True
    if A1[1] > l and A2[1] < m and A3[1] > A1[1]:
        return True
    if A2[0] == "z" and A3[1] <= l and A1[1] + A3[1] >= m:
        return True
    if A1[0] == "y" and A2[1] == l and A3[0] == "x" and A3[1] + A2[1] >= m:
        return True
    return False

