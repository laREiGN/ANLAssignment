import socket
import sys
import json

ServerIP = "145.24.222.103"
Port = 8001

class Client1:
    def __init__(self):
        self.clientid = None
    def connect(self, clientid):
        self.clientid = clientid
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ServerIP, Port))
        msgraw = s.recv(1024)
        msg = msgraw.decode("utf-8")
        print(msg)
        if "connection" in msg:
            reply = {}
            reply["studentnr"] = input("Please enter your student number: ")
            reply["classname"] = "INF2C"
            reply["clientid"] = self.clientid
            reply["teamname"] = "Gerrie en Timmie"
            reply["ip"] = socket.gethostbyname(socket.gethostname())
            reply["secret"] = None
            reply["status"] = None
            replyserialized = json.dumps(reply)
            s.send(bytes(replyserialized, "utf-8"))
            reply2 = s.recv(1024)
            reply2serialized = json.loads(reply2)
            print(reply2serialized["status"])
        s.close()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c2host = input("Enter the host name of client 2: ")
        c2port = 5000
        s.connect((c2host,c2port))
        s.send(bytes(json.dumps(reply2serialized), "utf-8"))

class Client2:
    def listen(self, clientid):
        self.clientid = clientid
        host = '0.0.0.0'
        port = 5000
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((host, port))
            print("Host name:", socket.gethostname())
        except socket.error as e:
            print(str(e))
        s.listen(5)
        conn, addr = s.accept()
        print('connected to: '+ addr[0]+':'+str(addr[1]))
        self.c1msg = conn.recv(1024).decode("utf-8")
        s.close()
        self.send()
    def send(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ServerIP, Port))
        c2msgjson = json.loads(self.c1msg)
        c2msgjson["studentnr"] = input("Please enter your student number: ")
        c2msgjson["clientid"] = self.clientid
        c2msgjson["ip"] = socket.gethostbyname(socket.gethostname())
        msgraw = s.recv(1024)
        msg = msgraw.decode("utf-8")
        print(msg)
        if "connection" in msg:
            c1replyserialized = json.dumps(c2msgjson)
            s.send(bytes(c1replyserialized, "utf-8"))
            c2reply = s.recv(1024)
            c2replyserialized = json.loads(c2reply)
            print(c2replyserialized['status'])
        



c1 = Client1()
c2 = Client2()


def Main():
    clientprompt = input("Which client do you want to use? Please only use 1 or 2: ")
    if clientprompt == "1":
        clientid = 1
        c1.connect(clientid)
    elif clientprompt == "2":
        clientid = 2
        c2.listen(clientid)
    else:
        print("Wrong client ID. Please try again.")
        Main()

Main()
