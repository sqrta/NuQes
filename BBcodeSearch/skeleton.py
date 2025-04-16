@funsearch.run
def funcScore():
    score = 0
    for key in allCodes.keys():
        l, m = key
        if l < 5 or m < 5:
            continue
        count = 0
        best = 0

        for code in allCodes[key]:
            A = code["A"]
            if priority(A, l, m):
                count += 1
                if code["d"] < 3:
                    continue
                r = code["k"] * code["d"] / code["n"]
                if r > best:
                    best = r

        if count > 1:
            score += best / ln(count)
    return score


@funsearch.evolve
def priority(A, l, m):
    return True
