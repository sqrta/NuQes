import os
import re
import json

folderPath = "database/"
fileNames = os.listdir(folderPath)


def jsonName(l, m):
    return f"l_{l}_m_{m}.json"


data = []


def dumpJson(l, m):
    # print(l,m)
    fileName = f"good_log_{l}_{m}_count33"
    if fileName not in fileNames:
        return []
    with open(folderPath + fileName, "r") as f:
        content = f.readlines()
    result = {"l": l, "m": m}
    codes = []
    for c in content:
        line = c.split(" ")
        nstr = re.findall(r"n: .*?,", c)
        if len(nstr) == 0:
            continue
        nstr = nstr[0]
        n = int(nstr[3:-1])
        kstr = re.findall(r"k: .*?,", c)[0]
        k = int(kstr[3:-1])
        dstr = re.findall(r"d: .*?,", c)[0]
        d = int(dstr[3:-1])
        ABstr = re.findall(r"r: .*?, .*?[,|\n]", c)[0].split(" ")

        def toTerm(string):
            res = []
            for i in string.split("+"):
                res.append((i[0], int(i[1:])))
            return res

        A = toTerm(ABstr[2][:-1])
        B = toTerm(ABstr[3][:-1])

        code = {"n": n, "k": k, "d": d, "A": A, "B": B}
        codes.append(code)
    with open("small/" + jsonName(l, m), "w") as f:
        json.dump(codes, f)


for file in fileNames:
    print(file)
    lm = file.split("_")
    print(lm)
    l = int(lm[2])
    m = int(lm[3])
    dumpJson(l, m)
# # dumpJson(16,7)
# exit(0)
