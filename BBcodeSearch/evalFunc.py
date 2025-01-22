from Priority import priority
import os
import json
from math import log as ln


def jsonName(l, m):
    return f"l_{l}_m_{m}.json"


def loadCode(l, m):
    with open("small/" + jsonName(l, m), "r") as f:
        codes = json.load(f)
    return codes


def getJsonlm(fileNames):
    file = fileNames.replace(".json", "")
    line = file.split("_")
    l = int(line[1])
    m = int(line[3])
    return l, m


allCodes = {}
jsonNames = os.listdir("small")
for file in jsonNames:
    l, m = getJsonlm(file)
    allCodes[(l, m)] = loadCode(l, m)


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


s = funcScore()
print(s)
with open("result", "w") as f:
    f.write(str(s))
