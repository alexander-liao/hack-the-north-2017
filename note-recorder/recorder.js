"use strict";

class Note {
    constructor(parsed, startTime) {
        this.parsed = parsed;
        this.startTime = startTime;
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
    getNoteByPitch(pitch) {
        for(var note of this.notes) {
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
            this.notes.push(new Note(parsed, currentTime / 1000));
        } else if(parsed["type"].toLowerCase() == "note off") {
            this.getNoteByPitch(parsed["pitch"]).end(currentTime / 1000);
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
