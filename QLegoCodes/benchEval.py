from progEval import *
import os
import numpy as np
from numpy import array
from numpy import int16

error = [(0.01, 0.05), (0.05, 0.01), (0.01, 0.01)]

for e in error:
    px, pz = e[0], e[1]
    print(f"px: {px}, pz: {pz}")
    path = f"foundBest/x_{int(px*100)}_z_{int(pz*100)}/"
    files = os.listdir(path)
    for file in files:
        nkStr = file.replace(".txt", "").split("_")
        n, k = int(nkStr[2]), int(nkStr[4])
        with open(path + file, "r") as f:
            code = eval(f.read())
        Hx, Hz = code["Hx"], code["Hz"]
        CM = np.concatenate((Hx, Hz), axis=1)
        stabilizers = checkM2Stabilizers(CM)
        TensorEnumerator = codeTN(stabilizers, isStab=True)
        error_rate = eval_code(stabilizers, k, px, pz)
        # error_rate = ABzx(stab_group, px, 1 - px, pz, 1 - pz, k)[1]
        print(f"n: {n}, k: {k}, error_rate: {error_rate}")
    print("")
