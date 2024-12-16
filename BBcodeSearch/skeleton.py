@funsearch.run
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


@funsearch.evolve
def priority(A, l, m):
    A1, A2, A3 = A[0], A[1], A[2]
    if A1[0] == "x" and A2[0] == "x" and A3[0] == "y" and int(A1[1]) + int(A2[1]) == l:
        return True
    return False
