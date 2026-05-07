import socket, time, json, threading, subprocess

# Load BPF object to trigger whatever
subprocess.run(['sudo', 'ip', 'link', 'set', 'dev', 'lo', 'xdp', 'off'])
subprocess.run(['sudo', 'ip', 'link', 'set', 'dev', 'lo', 'xdp', 'obj', 'diag.o', 'sec', 'prog'])

# Now fuzz the VSOCK endpoint with various payloads involving map_id
payloads = [
    {"map_id": 1},
    {"map_id": 2},
    {"map_id": 3},
    {"map_id": 4},
    {"map_id": 5},
    {"bpf_send_map_fds": 1},
    {"bpf_map_id": 1}
]

def send_payload(payload):
    for _ in range(20):
        try:
            s = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
            s.settimeout(0.5)
            s.connect((2, 9999))
            s.sendall(json.dumps(payload).encode() + b"\n")
            data = s.recv(1024)
            if data:
                with open("/tmp/vsock_success.txt", "a") as f:
                    f.write(f"Payload {payload} -> {data}\n")
            s.close()
            time.sleep(0.1)
        except Exception as e:
            time.sleep(0.1)

for p in payloads:
    threading.Thread(target=send_payload, args=(p,), daemon=True).start()

while True:
    time.sleep(1)
