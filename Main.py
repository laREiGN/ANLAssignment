import socket
import sys
import json

ServerIP = "145.24.222.103"
Port = 8001

class Main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ServerIP, Port))
    msgraw = s.recv(1024)
    msg = msgraw.decode("utf-8")
    print(msg)
    if "connection" in msg:
        reply = {}
        reply["studentnr"] = "123456"
        reply["classname"] = "INF2C"
        reply["clientid"] = 1
        reply["teamname"] = "Gerrie en Timmie"
        reply["ip"] = socket.gethostbyname(socket.gethostname())
        reply["secret"] = None
        reply["status"] = None
        replyserialized = json.dumps(reply)
        s.send(bytes(replyserialized, "utf-8"))
        reply2 = s.recv(1024)
        reply2serialized = json.loads(reply2)
        print(reply2serialized)



