var recorder = new (require("./recorder").Recorder)();
var fetch = require("node-fetch");

fetch(`http://localhost:5000/recorder/recording_start?pid=${process.pid}`)
    .then(res => res.json())
    .then(body => console.log(body));

process.stdin.setEncoding("utf8");
var lastInputTime = +new Date;
var haveOutputted = false;
// function resetKillTimeout() {
//     lastInputTime = +new Date;
//     killTimeout = setTimeout(() => {
//         if(+new Date - lastInputTime < 7000) {
//             return;
//         }
//         process.stdin.removeListener("data", stdinDataListener);
//         // Defined below
//         try {
//             if(!haveOutputted) {
//                 console.log(recorder.emitOutput());
//             }
//             haveOutputted = true;
//         } catch(e) {
//             console.log(e);
//         }
//         // console.log("Process exit");
//         // process.exit(0);
//         // setTimeout(() => {
//         // }, 100);
//     }, 7100);
// }
// Read data from stdin
// resetKillTimeout();
process.on("SIGUSR1", () => {
    var output = recorder.emitOutput();
    setTimeout(() => {
        console.log("Sending fetch");
        fetch("http://localhost:5000/recorder/set_recording_result", {
            method: "POST",
            body: output
        })
        .then(response => response.json())
        .then(body => {});
        console.log("Sent fetch");
    }, 5);
    console.log(output);
});
function stdinDataListener(line) {
    // if(JSON.parse(line)["type"] == "pid_headsup") {
    //     fetch(`http://localhost:5000/recorder/set_killee_process?pid=${JSON.parse(line)["pid"]}`)
    //         .then(response => response.json())
    //         .then(json => {});
    // }
    recorder.consumeLine(line);
    // resetKillTimeout();
}
process.stdin.on("data", stdinDataListener);
