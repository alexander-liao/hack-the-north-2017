# Chord Generator - Alexander Liao
# This will take dict input input (JSON format) for the harmonized melody and
# reorganize the outputs

# See /data-formats.md

# `python3 chordgenerator.py` -> `python3 satb.py`

import json
from sys import stdin

def transpose(data):
    return {
        "blocks": [
            {
                "score": component[0],
                "chords": list(zip(component[1], component[2]))
            } for component in data["blocks"]
        ]
    }

print(json.dumps(transpose(json.loads(stdin.read())), indent = 4))
