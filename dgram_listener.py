import socket, os, struct

sock_path = "/tmp/telemetry.sock"
if os.path.exists(sock_path):
    os.remove(sock_path)

sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
sock.bind(sock_path)

print("Listening...")
data, ancdata, flags, addr = sock.recvmsg(4096, 4096)
print("Received:", data)
print("Ancdata:", ancdata)
if ancdata:
    for cmsg_level, cmsg_type, cmsg_data in ancdata:
        if cmsg_level == socket.SOL_SOCKET and cmsg_type == socket.SCM_RIGHTS:
            fds = struct.unpack(f"{len(cmsg_data)//4}i", cmsg_data)
            print("FDs received:", fds)
