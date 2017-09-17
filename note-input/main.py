import subprocess
import sys
import re
import json
import os
import requests

requests.get("http://localhost:5000/recorder/set_killee_process?pid=%s" % os.getpid())

try:
    port = int(sys.argv[-1])
except:
    print("Usage:\npython3 main.py <port>")
    sys.exit(-1)

process = subprocess.Popen(["aseqdump", "-p", str(port)], stdout=subprocess.PIPE)

def parse_line(line):
    # line = re.sub("  +", "^", line.decode().strip())
    parts = re.split("  +", line.decode().strip())
    evt = parts[1] # Such as `Note on`, etc
    if len(parts) >= 3:
        properties = parts[2].split(", ")[1:]
    else:
        properties = []
    properties_dict = dict()
    for prop in properties:
        properties_dict[prop[:prop.index(" ")]] = prop[prop.index(" ") + 1:]
    if "velocity" in properties_dict:
        properties_dict["velocity"] = int(properties_dict["velocity"]) # Hack
    return dict(type=evt, pitch=int(properties_dict["note"]), **properties_dict)


process.stdout.readline()
process.stdout.readline()

# print(json.dumps(pid=os.getpid(), type="pid_headsup"))

for line in process.stdout:
    if "active sensing" not in line.decode().lower() and "clock" not in line.decode().lower():
        print(json.dumps(parse_line(line)))
    sys.stdout.flush()
