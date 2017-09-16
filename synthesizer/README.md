This is the MIDI synthesizer. It's written in Jython, and should be run using
the associated Jython jar. At some point, I want to rewrite this in `jjs` to
make it more portable.

This accepts note events in realtime on stdin.

To run:

`java -jar jython-standalone-2.7.0.jar main.py`
