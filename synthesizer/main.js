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
    java.lang.System.out.println("Line " + line.trim());
    var data = JSON.parse(line);
    if(data["type"].toLowerCase() == "note on") {
        channels[0].noteOn(data["pitch"], data["velocity"]);
    } else if(data["type"].toLowerCase() == "note off") {
        channels[0].noteOff(data["pitch"]);
    }
}
java.lang.System.out.println("Ended");
