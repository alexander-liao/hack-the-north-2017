# Preprocessor - Alexander Liao
# This will take dict input (JSON format) and assign each note a UUID

# See /data-formats.md

# `some input` -> `python3 chordgenerator.py`

import json
from sys import stdin, stdout
from chordoffsets import C, D, E, F, G, A, B

def snap(notes):
    sixteenthnote = notes["tempo"] / 4
    for note in notes["notes"]:
        note["startTime"] = round(note["startTime"] / sixteenthnote) * sixteenthnote
    return notes

def process(notes):
    uuid = 0
    for note in notes["notes"]:
        note["pitch"] -= notes["key"]
        note.update(uuid = uuid, octaves = note["pitch"] // 12)
        note["pitch"] %= 12
        uuid += 1
    notes["notes"].sort(key = lambda note: note["startTime"])
    notes["notes"] = list(filter(lambda note: note["pitch"] in [C, D, E, F, G, A, B], notes["notes"]))
    return notes

def merge(notes):
    combos = {}
    tempo = notes["tempo"]
    index = 0
    notelist = notes["notes"]
    for note in notelist:
        beat = int(note["startTime"] / tempo)
        if beat not in combos: combos[beat] = []
        combos[beat].append(note)
    return list(combos.values())

print(json.dumps(merge(process(snap(json.loads(stdin.read())))), indent = 4))
