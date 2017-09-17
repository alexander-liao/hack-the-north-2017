# Chord Generator - Alexander Liao
# This will take dict input input (JSON format) for the harmonized melody and
# reorganize the outputs

# See /data-formats.md

# `python3 chordgenerator.py` -> `python3 satb.py`

import json
from sys import stdin

def FT(obj):
    print(json.dumps(obj, indent = 4))
    return obj

def transpose(data):
    chunks = data["chunks"]
    result = []
    for chunk in chunks:
        chord = {}
        chord["score"] = chunk[0]
        chord["chords"] = []
        for chorddata, blocklist in zip(*chunk[1:]):
            for block in blocklist:
                chord["chords"].append((chorddata, block))
        result.append(chord)
    return {"blocks": result}

    '''
    return {
        "blocks": [
            {
                "score": component[0],
                "chords": list(zip(component[1], component[2]))
            } for component in data["blocks"]
        ]
    }
    '''

print(json.dumps(transpose(json.loads(stdin.read())), indent = 4))
