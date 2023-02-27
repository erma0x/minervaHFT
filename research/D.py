import subprocess
import os
import time
import threading

def run_command(cmd):
    p = subprocess.Popen(cmd, shell=True)
    time.sleep(5)
    os.kill(p.pid, 0.1)

cmd = "ping www.google.com"
thread = threading.Thread(target=run_command, args=(cmd,))
thread.start()
thread.join()