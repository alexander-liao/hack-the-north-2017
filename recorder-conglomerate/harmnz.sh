#!/bin/sh

python3 ../acc-gen/preprocessor.py | python3 ../acc-gen/chordgenerator.py | python3 ../acc-gen/interprocessor.py | python3 ../acc-gen/satb.py | python3 ../acc-gen/selector.py
