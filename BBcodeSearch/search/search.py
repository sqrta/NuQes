import numpy as np
from sympy import Matrix
from numpy.linalg import matrix_power as mp
import galois
import os
import sys
from interactive import *
from itertools import combinations
from functools import reduce
from gap_path import gap_path
from Priority import priority
from codeD import Get_kd_BBCode

import re


def replacenth(string, sub, wanted, n):
    where = [m.start() for m in re.finditer(sub, string)][n - 1]
    before = string[:where]
    after = string[where:]
    after = after.replace(sub, wanted, 1)
    newString = before + after
    return newString


GF = galois.GF(2)

int_range = 2
Terminal = ["l", "m"] + [str(i) for i in range(1, int_range + 1)]
Non_terminal = ["(S+S)", "(S-S)", "(S*S)", "min(S,S)", "max(S,S)", "S**S"]


class Statement:
    def __init__(self, init, depth) -> None:
        self.statement = init
        self.depth = depth

    def expand(self):
        result = []
        for i in range(1, self.depth + 1):
            for NT in Non_terminal:
                newOne = replacenth(self.statement, "S", NT, i)
                result.append(Statement(newOne, self.depth + 1))
        return result

    def terminate(self):
        result = []
        for T in Terminal:
            newOne = self.statement.replace("S", T, 1)
            result.append(Statement(newOne, self.depth - 1))
        return result


def get_candidate_state(MaxDepth):
    NT_list = [Statement("S", 1)]
    for i in range(MaxDepth):
        newList = []
        for statement in NT_list:
            newList += statement.expand()
        NT_list = newList
    result = []
    while len(NT_list) > 0:
        statement = NT_list.pop(0)
        if statement.depth == 0:
            result.append(statement.statement)
        else:
            NT_list += statement.terminate()
    return result


def get_S(l):
    M = GF(np.zeros((l, l), dtype=int))
    for i in range(l):
        M[i, (i + 1) % l] = 1
    return M


def get_I(l):
    return GF(np.identity(l, dtype=int))


def get_x(l, m):
    if m == 0:
        return get_S(l)
    if l == 0:
        return get_I(m)
    return np.kron(get_S(l), get_I(m))


def get_y(l, m):
    if m == 0:
        return get_I(l)
    if l == 0:
        return get_S(m)
    return np.kron(get_I(l), get_S(m))


def ker(M):
    return min(M.shape) - rank(M)


def rank(M):
    return np.linalg.matrix_rank(M)


def writeMatrix(path, M):
    save_dir = "./"
    shape = M.shape
    head = "%%MatrixMarket matrix coordinate integer general\n%% Field: GF(2)\n\n"
    with open(save_dir + path, "w") as f:
        f.write(head)
        f.write(f"{shape[0]} {shape[1]} {2*shape[1]}\n")
        for i in range(shape[0]):
            for j in range(shape[1]):
                if M[i, j] == 1:
                    f.write(f"{i+1} {j+1} 1\n")


def PowStr(p):

    return f"{p[0]}{p[1]}"


def sortFile(filename, key=("k", "d"), func=lambda k, d: k * d + d / 100.0):
    with open(filename, "r") as f:
        content = f.readlines()
        result = []
        for item in content:
            kstring = re.findall(rf"{key[0]}: [0-9]+,", item)[0]
            k = int(re.findall(r"[0-9]+", kstring)[0])
            kstring = re.findall(rf"{key[1]}: [0-9]+,", item)[0]
            d = float(re.findall(r"[0-9]+", kstring)[0])
            result.append((func(k, d), item))
        result.sort(key=lambda a: a[0], reverse=True)
    with open(filename, "w") as f:
        for item in result:
            f.write(item[1])


def combin(stuff, count):
    return list(combinations(stuff, count))


def good(n, k, d):
    r_frac = k * 1.0 / (2.0 * n)
    if (
        (d > (n / 16.0) and r_frac >= 3.0 / n)
        or (d > (n / 28.0) and r_frac > 4.0 / n)
        or d > 8
        or (d > 3 and k > 20)
    ):
        return True
    else:
        return False


def sumMat(mList):
    return reduce(lambda a, b: a + b, mList)


def pruneTerm(Terms, l, m):
    result = []

    for term in Terms:
        if priority(term, l, m):
            result.append(term)
    return result


def search_BBcode(l, m, countA, countB, kthres=4, init=0):
    filename = f"good_code_{l}_{m}.txt"
    ri, rj = init, 0
    if ri == 0 and rj == 0:
        with open(filename, "w") as f:
            pass
    else:
        with open(filename, "a") as f:
            pass
    gap = start([gap_path, "-L", "workplace", "-q", "-b"])
    power = get_candidate_state(1)
    power = [str(i) for i in range(6)]
    terms = [("x", i) for i in range(l)] + [("y", i) for i in range(1, m)]
    n = 2 * l * m
    x = get_x(l, m)
    y = get_y(l, m)
    result = []

    found = set()

    def mat(p):
        M = x if p[0] == "x" else y
        res = mp(M, p[1])
        return res

    def goodC(n, k, d):
        r = d * k * 1.0 / n
        if r > 0.5 or (k > n / 4 and d > 2) or (d > n / 6 and k > 5):
            return True
        return False

    term_len = len(terms)
    count = 0
    Aterms = combin(terms, countA)
    Aterms = pruneTerm(Aterms, l, m)
    # print(Aterms)
    for i in range(len(Aterms)):
        aterm = Aterms[i]
        print(f"{i}, {'+'.join([PowStr(a1) for a1 in aterm])}")

    iter_count = 0
    f = open(filename, "a")
    for i in range(ri, len(Aterms)):
        aterm = Aterms[i]
        print(f"i: {i}, iter: {iter_count},{'+'.join([PowStr(a1) for a1 in aterm])}")
        f.write(f"i: {i}, iter: {iter_count},{'+'.join([PowStr(a1) for a1 in aterm])}")
        A = sumMat([mat(t) for t in aterm])
        rankA = rank(A)
        if rankA >= l * m - kthres:
            print([PowStr(a1) for a1 in aterm], f"lm-rankA: {l*m-rankA}")

            continue
        if countA == countB:
            Bterms = Aterms[i:]
        else:
            Bterms = combin(terms, countB)
        jstart = rj if i == ri else 0
        for j in range(jstart, len(Bterms)):
            iter_count += 1
            bterm = Bterms[j]
            B = sumMat([mat(t) for t in bterm])
            k, d = Get_kd_BBCode(gap, A, B, l, m)
            r = d * k * 1.0 / n
            # print(f"i: {i}, j: {j} with n: {n}, k: {k}, d: {d}, r: {r}")
            # print(f"{iter_count},{'+'.join([PowStr(a1) for a1 in aterm])}, {'+'.join([PowStr(a1) for a1 in bterm])}")
            if True and goodC(n, k, d):
                # found.add((n,k,d))

                f.write((f"n: {n}, k: {k}, d: {d}, r: {r} code from: "))
                f.write(
                    f"A: {'+'.join([PowStr(a1) for a1 in aterm])}, B: {'+'.join([PowStr(a1) for a1 in bterm])}\n"
                )
            if k != 0:
                count += 1
            if count > 120:
                count = 1
                terminate(gap)
                gap = start([gap_path, "-L", "workplace", "-q", "-b"])

    print(f"itercount: {iter_count}")
    terminate(gap)
    sortFile(filename)
    f.close()
    return result


if __name__ == "__main__":

    toSearch = []
    countA = 4
    countB = 4
    flag = sys.argv[1]

    import time

    startT = time.time()
    countA = 3
    countB = 3
    kthres = 3
    l = int(sys.argv[1])
    m = int(sys.argv[2])
    print(f"search for l={l}, m={m}")
    res = search_BBcode(l, m, countA, countB, kthres)
    endT = time.time()

    print(f"use {endT-startT}s")
