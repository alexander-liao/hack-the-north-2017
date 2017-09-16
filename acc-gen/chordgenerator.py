# Chord Generator - Alexander Liao
# This will take dict input input (JSON format) for the completed melody and the
# list of prefabricated progressions

# See /data-formats.md

# `python3 preprocessor.py` -> `python3 satb.py`

import json
from chordoffsets import *
from sys import stdin

def match(progression, notes):
    chords = progression["chords"]
    if len(chords) > len(notes):
        return -1 # Don't match partial
    chorddata = [data[chord["type"]] for chord in chords]
    weight = 0
    for block, chord in zip(notes, chorddata):
        inner = 0
        for note in block:
            if note["pitch"] in chord[0]:
                inner += 4
            elif note["pitch"] in chord[1]:
                inner += 1
        weight += inner / len(block)
    return progression["weight"] * weight

selections = 3

def find(progressions, notes): # Top 3
    result = []
    for progression in progressions:
        score = match(progression, notes)
        if score != -1:
            chords = progression["chords"]
            result.append((score, chords, notes[:len(chords)]))
    return sorted(result)[:selections]

def generate(progressions, notes): # Top 3
    result = []
    for config in find(progressions, notes):
        for right in generate(progressions, notes[len(config[1]):]):
            score = config[0] + right[0]
            chords = config[1] + right[1]
            notes = config[2] + right[2]
            result.append((score, chords, notes))
    return sorted(result)[:selections]

print(json.dumps({
    "blocks": generate(
        json.loads(open("progressions.json", "r").read()),
        json.loads(stdin.read())
    )
}, indent = 4))
