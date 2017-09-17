#!/bin/sh

sleep 0.1

curl http://localhost:5000/playback/lasttoplay | python3 ../note-player/main.py | ncat localhost 1234 --send-only
