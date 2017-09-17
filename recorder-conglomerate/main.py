from flask import Flask, jsonify, request, make_response
from flask_sockets import Sockets
import json
import os
import signal
import subprocess

subprocess.Popen(os.path.join(os.path.dirname(os.path.realpath(__file__)), "synthd.sh"))

app = Flask(__name__)
sockets = Sockets(app)


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


last_to_play = None

@app.route("/playback/play", methods=["POST"])
def serve_playback_play():
    print("Serving /playback/play")
    global last_to_play
    last_to_play = request.get_data()
    print(os.path.join(os.path.dirname(os.path.realpath(__file__)), "playback.sh"))
    process = subprocess.Popen(os.path.join(os.path.dirname(os.path.realpath(__file__)), "playback.sh"))
    print(process.pid)
    # print(dir(process.stdin))
    # process.communicate(input=request.get_data())
    return jsonify(dict(success=True))

@app.route("/playback/lasttoplay")
def serve_last_to_play():
    print("last to play")
    return last_to_play


@app.route("/harmonize", methods=["POST"])
def serve_harmonize():
    return subprocess.check_output(os.path.join(os.path.dirname(os.path.realpath(__file__)), "harmnz.sh"), input=request.get_data()).decode()


if __name__ == "__main__":
    # app.run(port=5000)
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
