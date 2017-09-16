"use strict";

class Note {
    constructor(parsed, startTime) {
        this.parsed = parsed;
        this.startTime = startTime;
        this.duration = null;
    }
    end(endTime) {
        this.endTime = endTime;
        this.duration = this.endTime - this.startTime;
    }
    toJson() {
        this.parsed["startTime"] = this.startTime;
        this.parsed["duration"] = this.duration;
        this.parsed["endTime"] = this.endTime;
        return this.parsed;
    }
}
class Recorder {
    constructor() {
        this.notes = [];
        this.startTime = null;
        this.activeNotes = [];
    }
    getActiveNoteByPitch(pitch) {
        for(var note of this.activeNotes) {
            if(note.parsed["pitch"] == pitch) {
                return note;
            }
        }
    }
    consumeLine(line) {
        if(this.startTime == null) {
            this.startTime = +new Date;
        }
        var currentTime = +new Date - this.startTime;
        var parsed = JSON.parse(line);
        if(parsed["type"].toLowerCase() == "note on") {
            var note = new Note(parsed, currentTime / 1000);
            this.notes.push(note);
            this.activeNotes.push(note);
        } else if(parsed["type"].toLowerCase() == "note off") {
            var note = this.getActiveNoteByPitch(parsed["pitch"]);
            // console.log(parsed["pitch"], this.activeNotes.map(note => note.parsed["pitch"]))
            note.end(currentTime / 1000);
            this.activeNotes.splice(this.activeNotes.indexOf(note), 1);
        }
    }
    getTempo() {
        return this.notes[1].startTime - this.notes[0].startTime;
    }
    emitOutput() {
        var output = [];
        this.notes.forEach(line => output.push(line.toJson()));
        return JSON.stringify({
            "key": 60,
            "tempo": this.getTempo(),
            "notes": output
        }, null, 4);
    }
}

module.exports.Recorder = Recorder;
