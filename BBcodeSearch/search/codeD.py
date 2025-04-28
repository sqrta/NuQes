from interactive import *
from gap_path import gap_path
import numpy as np
import galois
from functools import reduce
from numpy.linalg import matrix_power as mp
import os

GF = galois.GF(2)


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


def get_distance(proc, Hx, Hz):

    writeMatrix(f"Hx.mtx", Hx)
    writeMatrix(f"Hz.mtx", Hz)
    write(proc, f'lisX:=ReadMTXE("Hx.mtx",0);;lisZ:=ReadMTXE("Hz.mtx",0);;\n')
    # write(proc, f'')
    write(proc, f"d:=DistRandCSS(lisX[3],lisZ[3],100,1,2:field:=GF(2));")
    # write(proc, "d;")
    result = read(proc)
    # print(f"res: {result}")
    d = int(result)
    return d


def rank(M):
    return np.linalg.matrix_rank(M)


def Get_kd_BBCode(proc, A, B, l, m):
    n = A.shape[0] * 2
    Hz = np.concatenate((B.T, A.T), axis=1)
    Hx = np.concatenate((A, B), axis=1)
    rankz = rank(Hz)
    k = n - 2 * rankz
    if k == 0:
        return 0, 0
    d = get_distance(proc, Hx, Hz)

    return k, d


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


def codeStr(code):
    return f"A: {'+'.join(code[0])}, B: {'+'.join(code[1])}"


def sumMat(mList):
    return reduce(lambda a, b: a + b, mList)


def mat(p):
    M = r if p[0] == "x" else s
    res = mp(M, int(p[1:]))
    return res


if __name__ == "__main__":
    gap = start([gap_path, "-L", "workplace", "-q", "-b"])
    l, m = 17, 5
    r = get_x(l, m)
    s = get_y(l, m)
    code1 = (["x1", "x16", "y4"], ["x4", "x13", "y1"])
    A = sumMat([mat(t) for t in code1[0]])
    B = sumMat([mat(t) for t in code1[1]])
    k, d = Get_kd_BBCode(gap, A, B, l, m)

    print(f"code with {codeStr(code1)} has n: {2*l*m}, k: {k}, d: {d}")
    os.system(f"rm *.mtx")

    gap = start([gap_path, "-L", "workplace", "-q", "-b"])
    l, m = 12, 12
    r = get_x(l, m)
    s = get_y(l, m)
    code1 = (["x1", "x2", "y9"], ["x3", "y5", "y10"])
    A = sumMat([mat(t) for t in code1[0]])
    B = sumMat([mat(t) for t in code1[1]])
    k, d = Get_kd_BBCode(gap, A, B, l, m)

    print(f"code with {codeStr(code1)} has n: {2*l*m}, k: {k}, d: {d}")
