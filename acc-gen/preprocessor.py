# Preprocessor - Alexander Liao
# This will take dict input (JSON format) and assign each note a UUID

# See /data-formats.md

# `some input` -> `python3 chordgenerator.py`

import json
from sys import stdin, stdout

def process(notes):
    uuid = 0
    for note in notes["notes"]:
        note["pitch"] -= notes["key"]
        note.update(uuid = uuid, octaves = note["pitch"] // 12)
        note["pitch"] %= 12
        uuid += 1
    return notes

print(json.dumps(process(json.loads(stdin.read()))))
