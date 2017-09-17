#!/bin/sh

# run this from hack-the-north-2017

python3 ../acc-gen/preprocessor.py | python3 ../acc-gen/chordgenerator.py "prog-new" | python3 ../acc-gen/interprocessor.py | python3 ../acc-gen/satb.py | python3 ../acc-gen/selector.py 0
# echo hi
