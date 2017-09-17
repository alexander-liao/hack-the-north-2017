# Selector - Alexander Liao
# This will select a harmony thing. This is for testing!

# See /data-formats.md

import json
from sys import stdin

print(json.dumps({
    "notes": json.loads(stdin.read())["blocks"][0]
}, indent = 4))
