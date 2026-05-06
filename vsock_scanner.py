import socket
import time
import os

CID = 2
PORT = 9999
SUCCESS_FILE = "/tmp/cid2_success.txt"

def attempt_connection():
    while not os.path.exists(SUCCESS_FILE):
        try:
            s = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
            s.settimeout(0.5)
            s.connect((CID, PORT))

            payload = b"FLAG{Bird_is_the_word_2026_Achei_o_design_simples_demais}"
            req = f"POST /telemetry HTTP/1.1\r\nHost: localhost\r\nContent-Type: text/plain\r\nContent-Length: {len(payload)}\r\n\r\n".encode() + payload
            s.sendall(req)
            data = s.recv(1024)
            if data:
                with open(SUCCESS_FILE, "wb") as f:
                    f.write(data)
                print(f"SUCCESS!")
            s.close()
        except Exception:
            pass
        time.sleep(0.1)

if __name__ == "__main__":
    attempt_connection()
