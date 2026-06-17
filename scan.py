import socket
for port in [22, 80, 443, 3000, 5000, 8000, 8080, 9000, 9999]:
    try:
        s = socket.socket()
        s.settimeout(0.2)
        s.connect(('192.168.0.1', port))
        print(f"Port {port} is open")
        s.close()
    except:
        pass
