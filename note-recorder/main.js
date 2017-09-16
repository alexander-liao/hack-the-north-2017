var recorder = new (require("./recorder").Recorder)();


process.stdin.setEncoding("utf8");
var lastInputTime = +new Date;
function resetKillTimeout() {
    lastInputTime = +new Date;
    killTimeout = setTimeout(() => {
        if(+new Date - lastInputTime < 7000) {
            return;
        }
        process.stdin.removeListener("data", stdinDataListener);
        // Defined below
        try {
            console.log(recorder.emitOutput());
        } catch(e) {
            console.log(e);
        }
        setTimeout(() => {
            process.exit(0);
        }, 10);
    }, 7100);
}
// Read data from stdin
resetKillTimeout();
function stdinDataListener(line) {
    recorder.consumeLine(line);
    resetKillTimeout();
}
process.stdin.on("data", stdinDataListener);
