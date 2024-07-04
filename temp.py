import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 9999  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.send("Hello, I am Client".encode('utf-8'))
    data = s.recv(65118)

print(f"JSON received: {data}")