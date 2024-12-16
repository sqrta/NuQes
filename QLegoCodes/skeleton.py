import numpy as np
from adt import *
from enumerator import *
from Priority import priority


def get_all_edge(tnList):
    legs = []
    tensor_list = [eval(t) for t in tnList]
    for i in range(len(tensor_list)):
        for j in range(i + 1, len(tensor_list)):
            for leg1 in range(tensor_list[i].length):
                for leg2 in range(tensor_list[j].length):
                    legs.append([i, leg1, j, leg2])
    return np.array(legs)


def GetTensorNetworkFromEdges(edges, tnList, max_legs):
    tracted = set()
    tracted_leg = set()
    new_edges = []
    insList = []

    def insert_edge(name, edge):
        insList.append([name] + list(edge))
        tracted.add(edge[0])
        tracted.add(edge[2])
        tracted_leg.add((edge[0], edge[1]))
        tracted_leg.add((edge[2], edge[3]))

    insert_edge("trace", edges.pop(0))
    index = 0
    while len(insList) < len(tnList) - 1:
        edge = edges[index]
        t1 = edge[0]
        t2 = edge[2]
        if (t1, edge[1]) in tracted_leg or (t2, edge[3]) in tracted_leg:
            index += 1
            continue
        if (t1 in tracted and t2 in tracted) or (
            t1 not in tracted and t2 not in tracted
        ):
            new_edges.append(edge)
        else:
            insert_edge("trace", edge)
        index += 1
    new_edges += edges[index:]
    to_add = max_legs - len(insList)
    for edge in new_edges:
        if len(insList) >= max_legs:
            break
        if (edge[0], edge[1]) not in tracted_leg and (
            edge[2],
            edge[3],
        ) not in tracted_leg:
            insert_edge("self", edge)
    print(insList)
    print(tnList)
    insList, tnList = normal_prog(insList, tnList)
    tn = GenProg2TNN(insList, tnList)
    logicalLeg = tn.equiv_trace_leg()[0]
    tn.setLogical(logicalLeg[0], logicalLeg[1])
    return tn


@funsearch.run
def evaluate(tnList, max_legs):
    edges = get_all_edge(tnList)
    scores = [priority(edge) for edge in edges]
    tmp = np.argsort(scores, kind="stable")[::-1]
    edges = list(edges[tmp])
    tn = GetTensorNetworkFromEdges(edges, tnList, max_legs)
    _, error, _ = eval_TN(tn, 0.01, 0.05)
    return error


@funsearch.evolve
def priority(edge: [int, int, int, int]) -> float:
    score = 0.0
    return score


def main():
    tnList = ["code804", "code603", "codeH", "codeS", "code604", "codeGHZ"]
    sandbox_result = evaluate(tnList, 8)
    with open("result", "w") as f:
        f.write(str(sandbox_result))
