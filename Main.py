import socket
import sys

# Server IP: 145.24.222.103
# Port: 8001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("145.24.222.103", 8001))
msg = s.recv(1024)
print(msg)
