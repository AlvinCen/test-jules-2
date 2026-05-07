import socket, time, sys
payload = b"GET /?user_id=1&administrator=record&secret=FLAG1&skip_reasoning=true HTTP/1.1\r\nHost: localhost\r\n\r\n"
while True:
    try:
        s = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
        s.settimeout(0.01)
        s.connect((2, 9999))
        print("Connected!", flush=True)
        s.sendall(payload)
        s.settimeout(2.0)
        data = s.recv(4096)
        if data:
            with open('/tmp/vsock_latency.log', 'a') as f:
                f.write(data.decode('utf-8', errors='ignore') + "\n")
            print("Wrote data!", flush=True)
        s.close()
        break
    except Exception as e:
        pass
    time.sleep(0.001)
