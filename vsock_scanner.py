import socket
import time

def main():
    while True:
        try:
            s = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
            s.settimeout(0.5)
            s.connect((2, 9999))
            s.sendall(b"{\"telemetry\": 123}")
            data = s.recv(1024)
            s.close()
        except Exception:
            pass
        time.sleep(0.1)

if __name__ == "__main__":
    main()
