# Preprocessor - Alexander Liao
# This will take dict input (JSON format) and assign each note a UUID

# See /data-formats.md

# `some input` -> `python3 chordgenerator.py`

import json
from sys import stdin, stdout

def snap(notes):
    tempo = notes["tempo"] * 4
    for note in notes["notes"]:
        note["startTime"] = round(note["startTime"] * tempo) / tempo
    return notes

def process(notes):
    uuid = 0
    for note in notes["notes"]:
        note["pitch"] -= notes["key"]
        note.update(uuid = uuid, octaves = note["pitch"] // 12)
        note["pitch"] %= 12
        uuid += 1
    print(notes)
    return sorted(notes["notes"], key = lambda note: note["startTime"])

def merge(notes):
    combos = []
    beat = 0
    tempo = notes["tempo"]
    index = 0
    notelist = notes["notes"]
    while beat <= notelist[-1]["startTime"]:
        combo = []
        while index <= len(notelist):
            if notelist[index]["startTime"] < beat + tempo:
                combo.append(notelist[index])
            else:
                beat += tempo
                break
        combos.append(combo)
    return combos

print(json.dumps(process(snap(json.loads(stdin.read()))), indent = 4))
