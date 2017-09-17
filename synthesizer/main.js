var reader = new java.io.BufferedReader(new java.io.InputStreamReader(java.lang.System.in));

var synth = javax.sound.midi.MidiSystem.getSynthesizer();
synth.open();

var channels = synth.getChannels();
instruments = synth.getDefaultSoundbank().getInstruments();

java.lang.System.out.println("Initialized");

while(true) {
    var line = reader.readLine();
    if(line == null) {
        break;
    }
    var data = JSON.parse(line);
    java.lang.System.out.println(data["velocity"] ? ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"][data["pitch"] % 12] : "--");
    if(data["type"].toLowerCase() == "note on") {
        channels[0].noteOn(data["pitch"], data["velocity"]);
    } else if(data["type"].toLowerCase() == "note off") {
        channels[0].noteOff(data["pitch"]);
    }
}
java.lang.System.out.println("Ended");
