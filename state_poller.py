import socket
import time
import os

AF_VSOCK = getattr(socket, "AF_VSOCK", 40)

def poll():
    cid = 2
    port = 9999
    log_file = "/tmp/poller.log"
    heartbeat_file = "/tmp/heartbeat.log"
    count = 0
    while True:
        try:
            s = socket.socket(AF_VSOCK, socket.SOCK_STREAM)
            s.settimeout(0.2)
            s.connect((cid, port))
            with open(log_file, "a") as f:
                f.write(f"[{time.ctime()}] FIREWALL OPEN\n")
            s.close()
        except Exception as e:
            # Optionally log errors to a debug file
            with open("/tmp/poller_debug.log", "a") as f:
                f.write(f"[{time.ctime()}] Attempt {count}: {type(e).__name__}: {e}\n")

        count += 1
        if count % 10 == 0:
            with open(heartbeat_file, "w") as f:
                f.write(f"Heartbeat at {time.ctime()}, count {count}\n")

        # No sleep or very short sleep for high frequency
        # time.sleep(0.01)
