import sys
import time
import threading

class PrintThread(threading.Thread):
    def __init__(self, text, delay):
        threading.Thread.__init__(self)
        self.text = text
        self.delay = delay

    def run(self):
        time.sleep(self.delay)
        sys.stdout.write(self.text)
        sys.stdout.flush()

try:
    delay = float(sys.argv[-1])
except:
    print("Usage:\npython3 main.py <delay>")
    sys.exit(-1)

for line in sys.stdin:
    PrintThread(line, delay).start()
