from flask import Flask, jsonify, request, make_response
import json
import os
import signal
import subprocess

app = Flask(__name__)


recording_pid = -1
most_recent_recording = None
killee_process = -1


@app.route("/recorder/recording_start")
def serve_recorder_recording_start():
    global recording_pid
    recording_pid = int(request.args.get("pid"))
    return jsonify(dict(success=True))

@app.route("/recorder/create_recording")
def serve_recorder_create_recording():
    # We just discard the Popen object, we don't need it
    print(os.path.join(os.path.dirname(os.path.realpath(__file__)), "record.sh"), __file__)
    subprocess.Popen(os.path.join(os.path.dirname(os.path.realpath(__file__)), "record.sh"))
    return jsonify(dict(success=True))

@app.route("/recorder/get_pid")
def serve_recorder_get_pid():
    return jsonify(dict(success=True, pid=recording_pid, killee=killee_process))

@app.route("/recorder/finish")
def serve_recorder_recording_finish():
    os.kill(recording_pid, signal.SIGUSR1)
    return jsonify(dict(success=True))

@app.route("/recorder/set_recording_result", methods=["POST"])
def serve_set_recording_result():
    global most_recent_recording
    most_recent_recording = request.get_data()
    print("Set recording result")
    os.kill(killee_process, signal.SIGTERM)
    os.kill(recording_pid, signal.SIGTERM)
    return jsonify(dict(success=True))

@app.route("/recorder/set_killee_process")
def serve_set_killee_process():
    global killee_process
    killee_process = int(request.args.get("pid"))
    return jsonify(dict(success=True))

@app.route("/recorder/recording_result")
def serve_recording_result():
    return most_recent_recording or "nothing"


if __name__ == "__main__":
    app.run(port=5000)
