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
        note["tempo"] = notes["tempo"]
        note["key"] = notes["key"]
        note.update(uuid = uuid, octaves = note["pitch"] // 12)
        note["pitch"] %= 12
        uuid += 1
    notes["notes"].sort(key = lambda note: note["startTime"])
    # for note in notes["notes"]: # Magic code apparently is not magic
        # note["invisible"] = note["pitch"] not in [C, D, E, F, G, A, B] # Magic Ethan code
    # notes["notes"] = filter(lambda note: note["pitch"] in [C, D, E, F, G, A, B], notes["notes"]) # this sounds bad?
    return notes

def equal(block1, block2):
    if block2 == None:
        return False
    head1 = block1[0]
    head2 = block2[0]
    return head1["startTime"] - head2["startTime"] == head1["tempo"] and [note["pitch"] for note in block1] == [note["pitch"] for note in block2]

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

def metamerge(blocks):
    chunks = []
    for block in blocks:
        if len(chunks) > 0 and equal(block, chunks[-1][-1]):
            chunks[-1].append(block)
        else:
            chunks.append([block])
    return chunks

print(json.dumps(metamerge(merge(process(snap(json.loads(stdin.read()))))), indent = 4))
