from flask import Flask, jsonify, request, make_response, abort
import json

app = Flask(__name__)

state = "idle"

recording = """
{
    "key": 60,
    "tempo": 0.273,
    "notes": [
        {
            "velocity": 113,
            "note": "55",
            "type": "Note on",
            "pitch": 55,
            "startTime": 0,
            "duration": 0.325,
            "endTime": 0.325
        },
        {
            "velocity": 120,
            "note": "57",
            "type": "Note on",
            "pitch": 57,
            "startTime": 0.273,
            "duration": 0.31199999999999994,
            "endTime": 0.585
        },
        {
            "velocity": 122,
            "note": "59",
            "type": "Note on",
            "pitch": 59,
            "startTime": 0.54,
            "duration": 0.29399999999999993,
            "endTime": 0.834
        },
        {
            "velocity": 112,
            "note": "60",
            "type": "Note on",
            "pitch": 60,
            "startTime": 0.825,
            "duration": 0.28500000000000014,
            "endTime": 1.11
        },
        {
            "velocity": 122,
            "note": "62",
            "type": "Note on",
            "pitch": 62,
            "startTime": 1.115,
            "duration": 0.40900000000000003,
            "endTime": 1.524
        },
        {
            "velocity": 122,
            "note": "64",
            "type": "Note on",
            "pitch": 64,
            "startTime": 1.489,
            "duration": 0.29499999999999993,
            "endTime": 1.784
        },
        {
            "velocity": 123,
            "note": "66",
            "type": "Note on",
            "pitch": 66,
            "startTime": 1.754,
            "duration": 0.30900000000000016,
            "endTime": 2.063
        },
        {
            "velocity": 120,
            "note": "67",
            "type": "Note on",
            "pitch": 67,
            "startTime": 2.063,
            "duration": 0.3139999999999996,
            "endTime": 2.377
        },
        {
            "velocity": 123,
            "note": "66",
            "type": "Note on",
            "pitch": 66,
            "startTime": 2.342,
            "duration": 0.35299999999999976,
            "endTime": 2.695
        },
        {
            "velocity": 121,
            "note": "64",
            "type": "Note on",
            "pitch": 64,
            "startTime": 2.664,
            "duration": 0.30200000000000005,
            "endTime": 2.966
        },
        {
            "velocity": 123,
            "note": "62",
            "type": "Note on",
            "pitch": 62,
            "startTime": 2.954,
            "duration": 0.2869999999999999,
            "endTime": 3.241
        },
        {
            "velocity": 123,
            "note": "60",
            "type": "Note on",
            "pitch": 60,
            "startTime": 3.223,
            "duration": 0.3120000000000003,
            "endTime": 3.535
        },
        {
            "velocity": 124,
            "note": "59",
            "type": "Note on",
            "pitch": 59,
            "startTime": 3.511,
            "duration": 0.3039999999999998,
            "endTime": 3.815
        },
        {
            "velocity": 123,
            "note": "57",
            "type": "Note on",
            "pitch": 57,
            "startTime": 3.782,
            "duration": 0.29499999999999993,
            "endTime": 4.077
        },
        {
            "velocity": 122,
            "note": "55",
            "type": "Note on",
            "pitch": 55,
            "startTime": 4.081,
            "duration": 0.18599999999999994,
            "endTime": 4.267
        }
    ]
}
"""
recording = json.loads(recording)

@app.route("/recorder/create_recording")
def serve_recordercreate_recording():
    global state
    state = "created_recording"
    return jsonify(dict(success=True))

@app.route("/recorder/get_pid")
def serve_recorder_get_pid():
    if state not in ["idle", "finished"]:
        return jsonify(dict(success=True, pid=599, killee=499))
    else:
        return jsonify(dict(success=True, pid=-1, killee=-1))

@app.route("/recorder/finish")
def serve_recorder_finish():
    global state
    if state != "created_recording":
        abort(400)
    state = "finished"
    return jsonify(dict(success=True))

@app.route("/recorder/recording_result")
def serve_recorder_recording_result():
    if state != "finished":
        abort(400)
    return jsonify(recording)

if __name__ == "__main__":
    app.run(port=5000)
