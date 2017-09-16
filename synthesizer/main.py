from javax.sound.midi import MidiSystem
import json
import sys

synth = MidiSystem.getSynthesizer()
synth.open()

channels = synth.getChannels()
instruments = synth.getDefaultSoundbank().getInstruments()

# channels[0].noteOn(60, 127)
# channels[0].noteOff(60, 127)

print("Loaded")

for line in sys.stdin:
    print(line.strip())
    data = json.loads(line)
    if data["type"].lower() == "note on":
        channels[0].noteOn(data["pitch"], data["velocity"])
    elif data["type"].lower() == "note off":
        channels[0].noteOff(data["pitch"])
