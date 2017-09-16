# SATB - Alexander Liao
# This will take dict input input (JSON format) for the harmonized melody and
# order the voices

# See /data-formats.md

# `python3 interprocessor.py` -> `python3 postprocessor.py`

import json
from sys import stdin
from chordoffsets import *

def paths(matrix):
    if len(matrix) == 0:
        return []
    elif len(matrix) == 1:
        return [[x] for x in matrix[0]]
    else:
        return [[x] + y for x in matrix[0] for y in paths(matrix[1:])]

def getChords(S, A, T, B, V, R):
    s = S and [S] or V
    a = A and [A] or V
    t = T and [T] or V
    b = B and [B] or V
    return list(filter(lambda x: all(r in x for r in R), paths([s, a, t, b])))

def genData(current, last):
    S = current[1]
    print(":", S["pitch"])
    return current

def SATB(data):
    chords = data["chords"]
    last = None
    print(len(chords))
    for chord in chords:
        chorddata = chord[0]
        soprano = chord[1][0]
        current = (chorddata, soprano)
        last = genData(current, last)
    return data

print(json.dumps({
    "blocks": [SATB(prog) for prog in json.loads(stdin.read())["blocks"]]
}, indent = 4))
