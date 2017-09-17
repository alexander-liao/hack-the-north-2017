#!/bin/sh

ncat -l 1234 -k --recv-only | jjs ../synthesizer/main.js
