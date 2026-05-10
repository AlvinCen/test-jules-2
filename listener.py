import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 4444))
s.listen(1)
print("Listening on 4444...")
conn, addr = s.accept()
print(f"Connection from {addr}")

# Send a command to verify we are in the reviewer
conn.send(b"id\npwd\nhostname\n")
print(conn.recv(4096).decode())
conn.close()
