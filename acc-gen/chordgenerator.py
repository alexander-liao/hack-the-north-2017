# Chord Generator - Alexander Liao
# This will take dict input input (JSON format) for the completed melody and the
# list of prefabricated progressions

# See /data-formats.md

# `python3 preprocessor.py` -> `python3 satb.py`

import json
from chordoffsets import *

def match(progression, notes):
    chords = progression["chords"]
    if len(chords) > len(notes):
        return -1 # Don't match partial
    chorddata = [data[chord["type"]] for chord in chords]
    return progression["weight"] * sum(
        4 if note["pitch"] in chord[0]
        else 2 if note["pitch"] in chord[1]
        else 0 for note, chord in zip(notes, chorddata)
    )

def generate(progressions, notes):
    index = 0
    while index < len(notes):
        pass
