import codecs
import sys
import numpy as np
import random
import math
import pprint
from itertools import chain, combinations

strmap = {
    "0": "₀", "1": "₁", "2": "₂", "3": "₃", "4": "₄", "5": "₅", "6": "₆",
    "7": "₇", "8": "₈", "9": "₉",
    "lambda": "\u03BB", "alpha": "\u03B1", "beta": "\u03B2", "rho": "\u03C1",
    "Qbar" : u'Q\u0305', 'bar' : u'\u0305',
    "in" : 	u"\u2208", "pi" : u"\u03C0", "notequal" : u"\u2260",
    "tau" : u"\u03C4",
    "epsilon" : u"\u03B5", "Delta" : u"\u0394", "gamma": u"\u03B3",
    "Gamma": u"\u0393"
}

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def godelproduct(a,b):
    if a <= b:
        return 1
    else:
        return b

def godelconjunction(a,b):
    if a <= (1 - b):
        return 0
    else:
        return b

def structInit(n):
    q = {}
    z = [i for i in range(1,n+1)]
    r = powerset(z)

    for i in r:
            q[frozenset(i)] = {
                "criteria": frozenset(i),
                "xi": ["x"+strmap[str(j)] for j in i],
                "complement": frozenset(set(z).difference(set(i))),
                "value": 0
            }
    return q

def setSimpleCapacity(n,capacity):
    z = [i for i in range(1,n+1)]
    r = powerset(z)

    for s in capacity:
        if len(s) == n:
            capacity[s]["value"] = 1
            continue
        if len(s) == 0:
            capacity[s]["value"] = 0
            continue
        capacity[s]["value"] = float(len(s))/float(n)

    return capacity

def getConjugateCapacity(n,capacity):
    z = [i for i in range(1,n+1)]
    r = powerset(z)
    conjugate = capacity
    for s in capacity:
        conjugate[s]["value"] = 1 - capacity[s]["value"]

    return conjugate


def setminXi(n,L):
    Xi = structInit(n)
    for k in Xi:
        if k == frozenset():
            continue
        Xi[k]["value"] = min([L[u] for u in k])

    return Xi

def setmaxXi(n,L):
    Xi = structInit(n)
    for k in Xi:
        if k == frozenset():
            continue
        Xi[k]["value"] = max([L[u] for u in k])
    return Xi

def OpposedXi(Xi):
    Xi2 = Xi
    for k in Xi:
        Xi2[k]["value"] = 1 - Xi[k]["value"]
    return Xi2



def GodelIntegralImplication(n,capacity,L):
    Xi = setmaxXi(n,L)
    z = [i for i in range(1,n+1)]
    r = powerset(z)
    data = []
    for i in r:
        a = 1 - capacity[frozenset(i)]["value"] # conjugate
        b = Xi[frozenset(i)]["value"]
        data.append(godelproduct(a,b))

    return min(data)

def GodelIntegralConjunction(n,capacity,L):
    Xi = setminXi(n,L)
    z = [i for i in range(1,n+1)]
    r = powerset(z)
    data = []
    for i in r:
        a = capacity[frozenset(i)]["value"]
        b = Xi[frozenset(i)]["value"]
        data.append(godelconjunction(a,b))

    return max(data)

def checkPropertyDuality(n,capacity,L):
    Xi = setmaxXi(n,L)
    OXi = OpposedXi(Xi)
    z = [i for i in range(1,n+1)]
    r = powerset(z)
    data = []

    conjugate = getConjugateCapacity(n,capacity)
    for i in r:
        a = 1 - conjugate[frozenset(i)]["value"] # conjugate
        b = OXi[frozenset(i)]["value"]
        data.append(godelproduct(a,b))

    OpposedImpGodelConjugateOppposed = 1 - min(data)
    ClassicalGodelConj = GodelIntegralConjunction(n,capacity,L)
    print(OpposedImpGodelConjugateOppposed)
    print(ClassicalGodelConj)



def main():
    n = 3
    L = {
        1: 0.3,
        2: 0.7,
        3: 0.2
    }
    """
    capacity = structInit(n)
    capacity = setSimpleCapacity(n,capacity)
    pprint.pprint(L)
    pprint.pprint(capacity)

    xImplication = GodelIntegralImplication(n,capacity,L)
    xConjunction = GodelIntegralConjunction(n,capacity,L)

    print(xImplication)
    print(xConjunction)


    checkPropertyDuality(n,capacity,L)
    """
    a = 0.81
    b = 0.2
    print(godelconjunction(a,b))




if __name__ == "__main__":
    main()
