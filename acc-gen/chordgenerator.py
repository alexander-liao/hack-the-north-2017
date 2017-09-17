# Chord Generator - Alexander Liao
# This will take dict input (JSON format) for the completed melody and the list
# of prefabricated progressions

# See /data-formats.md

# `python3 preprocessor.py` -> `python3 interprocessor.py`

import json
from chordoffsets import *
from sys import stdin, argv

def equal(block1, block2):
    if block2 == None:
        return False
    head1 = block1[0]
    head2 = block2[0]
    return head1["startTime"] - head2["startTime"] == head1["tempo"] and [note["pitch"] for note in block1] == [note["pitch"] for note in block2]

def match(progression, notes):
    chords = progression["chords"]
    if len(chords) > len(notes):
        return -1 # Don't match partial
    chorddata = [data[chord["type"]] for chord in chords]
    weight = 0
    bindex = 0
    cindex = 0
    last = None
    while cindex <= bindex < len(chorddata):
        block = notes[bindex]
        chord = chorddata[cindex]
        inner = 0
        for note in block:
            if note["pitch"] in chord[0]:
                inner += 8
            elif note["pitch"] in chord[1]:
                inner -= 4
            else:
                inner -= 8
                # return -1
        weight += inner / len(block)
        bindex += 1
        if not equal(block, last) or len(chorddata) - cindex == len(notes) - bindex:
            cindex += 1
        last = block
    if len(notes) == bindex and chords[-1]["type"] != "I":
        return -1
    return progression["weight"] + weight * 25

selections = 1

def find(progressions, notes): # Top 3
    result = []
    for progression in progressions["progressions"]:
        score = match(progression, notes)
        if score != -1:
            chords = progression["chords"]
            result.append((score, chords, notes[:len(chords)]))
    return sorted(result, key = lambda node: node[0])[-selections:]

def generate(progressions, notes): # Top 3
    result = []
    for config in find(progressions, notes):
        if len(notes) > len(config[1]):
            for right in generate(progressions, notes[len(config[1]):]):
                score = config[0] + right[0]
                chords = config[1] + right[1]
                notes = config[2] + right[2]
                result.append((score, chords, notes))
        else:
            result.append(config)
    return sorted(result, key = lambda node: node[0])[-selections:]

import os
path = os.path.dirname(__file__)

print(json.dumps({
    "blocks": generate(
        json.loads(open(path + "/" + argv[1] + ".json", "r").read()),
        json.loads(stdin.read())
    )
}, indent = 4))
