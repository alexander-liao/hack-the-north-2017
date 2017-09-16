import time
import sys
import json

data = json.loads(sys.stdin.read())

class Action:
    def __init__(self, time, type, **data):
        self.time = time
        self.type = type
        self.data = data

    def emit(self):
        datacpy = self.data.copy()
        datacpy["type"] = self.type
        return datacpy

actions = []

for note in data["notes"]:
    actions.append(Action(note["startTime"], "Note on", pitch=note["pitch"], velocity=note["velocity"]))
    actions.append(Action(note["startTime"] + note["duration"], "Note off", pitch=note["pitch"]))

actions.sort(key=lambda action: action.time)

start_time = time.time()
for action in actions:
    current_time = time.time() - start_time
    diff = max(action.time - current_time, 0)
    time.sleep(diff)
    print(json.dumps(action.emit()))
    sys.stdout.flush()
