#!/bin/sh

while true; do
    ncat -l 1234 -k --recv-only | jjs ../synthesizer/main.js
done
