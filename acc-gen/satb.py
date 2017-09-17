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
    s = [S] if S is not None else V
    a = [A] if A is not None else V
    t = [T] if T is not None else V
    b = [B] if B is not None else V
    return list(filter(lambda x: all(r in x for r in R), paths([s, a, t, b])))

def score(chorddata, chord, last):
    points = len(set(chord))
    if chord[-1] == data[chorddata["type"]][0][0]:
        points *= 2
    return points

def genData(current, last):
    chorddata = current[0]
    V = data[chorddata["type"]]
    V, R = V[::2]
    S = current[1]["pitch"]
    B = None
    if chorddata["inversion"] != -1:
        B = V[chorddata["inversion"] % len(V)]
    chords = getChords(S, None, None, B, V, R)
    return max(chords, key = lambda chord: score(chorddata, chord, last))[1:]

def SATB(data):
    chords = data["chords"]
    last = None
    harmony = []
    for chord in chords:
        chorddata = chord[0]
        soprano = chord[1][0]
        current = (chorddata, soprano)
        last = genData(current, last)
        harmony.append(last)
        active_notes = chord[1]
        for note in active_notes:
            note["pitch"] += note["octaves"] * 12
            note["pitch"] += note["key"]
            harmony[-1] = [pitch + note["key"] - 12 for pitch in harmony[-1]]
        harmony[-1] = [{
            "velocity": int(active_notes[0]["velocity"] * 0.75),
            "duration": active_notes[-1]["duration"] + active_notes[-1]["startTime"] - active_notes[0]["startTime"],
            "startTime": active_notes[0]["startTime"],
            "pitch": pitch
        } for pitch in harmony[-1]]
        harmony[-1] += active_notes
    return sum(harmony, [])

print(json.dumps({
    "blocks": [SATB(prog) for prog in json.loads(stdin.read())["blocks"]]
}, indent = 4))
