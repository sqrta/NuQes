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
    return True
