import socket
import sys

ServerIP = "145.24.222.103"
Port = 8001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ServerIP, Port))
msgraw = s.recv(1024)
msg = msgraw.decode("utf-8")
print(msg)

